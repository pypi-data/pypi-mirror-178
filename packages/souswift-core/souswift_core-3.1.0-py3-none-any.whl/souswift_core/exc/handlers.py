import http
from typing import Union

import fastapi
import fastapi.responses

from souswift_core import models
from souswift_core.exc import exceptions, ext

_Exception = Union[
    exceptions.APIError, exceptions.DatabaseError, ext.ExtendedError
]


def _api_error_handler(request: fastapi.Request, exc: exceptions.APIError):
    exc_response = exc.response()
    return fastapi.responses.ORJSONResponse(
        models.BaseError(
            title=type(exc).__name__.lower(),
            path=request.url.path,
            status=exc_response.status_code,
            detail=exc_response.message,
        ).dict(by_alias=True),
        status_code=exc_response.status_code,
    )


def _database_error_handler(
    request: fastapi.Request, exc: exceptions.DatabaseError
):
    exc_response = exc.response()
    return fastapi.responses.ORJSONResponse(
        models.BaseError(
            title=type(exc).__name__.lower(),
            path=request.url.path,
            status=exc_response.status_code,
            detail=exc_response.message,
        ).dict(by_alias=True),
        status_code=exc_response.status_code,
    )


def _extended_error_handler(request: fastapi.Request, exc: ext.ExtendedError):
    exc_response = exc.response()
    return fastapi.responses.ORJSONResponse(
        models.ExtendedBaseError(
            title=type(exc).__name__.lower(),
            path=request.url.path,
            status=exc_response.status_code,
            detail=exc_response.message,
            error_key=exc_response.error_key,
        ).dict(by_alias=True),
        status_code=exc_response.status_code,
    )


def _base_exception_handler(request: fastapi.Request, exc: Exception):
    status = http.HTTPStatus.INTERNAL_SERVER_ERROR
    return fastapi.responses.ORJSONResponse(
        models.BaseError(
            title='exception',
            path=request.url.path,
            status=status,
            detail='Internal Server Error',
        ).dict(by_alias=True),
        status_code=status,
    )


def add_exception_handlers(
    app: fastapi.FastAPI,
    *exclude: type[_Exception],
    exclude_base_exception_handler: bool = False
):
    for exception, handler in (
        (exceptions.APIError, _api_error_handler),
        (exceptions.DatabaseError, _database_error_handler),
        (ext.ExtendedError, _extended_error_handler),
    ):
        if exception in exclude:
            continue
        app.add_exception_handler(exception, handler)
    if not exclude_base_exception_handler:
        app.add_exception_handler(Exception, _base_exception_handler)
