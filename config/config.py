import os

from loguru import logger


DEFAULT_URLS = {
    "dev": "https://dev-api.myqrcards.com",
    "prod": "https://api.myqrcards.com",
}


def get_host() -> str:
    environ = os.getenv("ENVIRON", "dev").lower()
    if environ not in DEFAULT_URLS:
        raise ValueError(f"Unsupported environment: {environ}")

    host = (
        os.getenv("HOST")
        or os.getenv(f"URL_{environ.upper()}_API")
        or DEFAULT_URLS[environ]
    ).rstrip("/")
    if not host:
        raise ValueError(f"Invalid or missing URL for environment: {environ}")
    return host


ENVIRON = os.getenv("ENVIRON", "dev").lower()
HOST = get_host()

logger.debug(f"[ENVIRON] Active environment: {ENVIRON}")
logger.debug(f"[HOST] Base URL: {HOST}")
