from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.logging import logger


async def unexpected_exception_handler(
    request: Request,
    exc: Exception,
):
    logger.exception(
        "Unexpected application error",
        exc_info=exc,
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
        },
    )