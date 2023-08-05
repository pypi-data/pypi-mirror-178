import logging
import re
from contextvars import ContextVar
from re import RegexFlag
from typing import Any, Dict, Optional, Set

from aiohttp import web
from aiohttp.web import Request, StreamResponse
from aiohttp.web import middleware
from resotolib import jwt as ck_jwt
from jwt import PyJWTError

from resotolib.asynchronous.web import RequestHandler, Middleware

log = logging.getLogger(__name__)
JWT = Dict[str, Any]
__JWT_Context: ContextVar[JWT] = ContextVar("JWT", default={})


async def jwt_from_context() -> JWT:
    """
    Inside a request handler, this value retrieves the current jwt.
    """
    return __JWT_Context.get()


@middleware
async def no_check(request: Request, handler: RequestHandler) -> StreamResponse:
    return await handler(request)


def check_jwt(psk: str, always_allowed_paths: Set[str]) -> Middleware:
    def always_allowed(request: Request) -> bool:
        for path in always_allowed_paths:
            if re.fullmatch(path, request.path, RegexFlag.IGNORECASE):
                return True
        return False

    @middleware
    async def valid_jwt_handler(request: Request, handler: RequestHandler) -> StreamResponse:
        auth_header = request.headers.get("authorization") or request.cookies.get("resoto_authorization")
        if always_allowed(request):
            return await handler(request)
        elif auth_header:
            try:
                # note: the expiration is already checked by this function
                jwt = ck_jwt.decode_jwt_from_header_value(auth_header, psk)
            except PyJWTError as ex:
                raise web.HTTPUnauthorized() from ex
            if jwt:
                __JWT_Context.set(jwt)
                return await handler(request)
        # if we come here, something is wrong: reject
        raise web.HTTPUnauthorized()

    return valid_jwt_handler


def auth_handler(psk: Optional[str], always_allowed_paths: Set[str]) -> Middleware:
    if psk:
        log.info("Use JWT authentication with a pre shared key")
        return check_jwt(psk, always_allowed_paths)
    else:
        log.info("No authentication requested.")
        return no_check
