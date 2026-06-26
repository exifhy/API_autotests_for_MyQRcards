import os

from loguru import logger


DEFAULT_URLS = {
    "dev": "https://dev-api.myqrcards.com",
    "prod": "https://api.myqrcards.com",
}

DEFAULT_UPLOAD_URLS = {
    "dev": "https://dev-upload.myqrcards.com",
    "prod": "https://upload.myqrcards.com",
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


def get_upload_host() -> str:
    environ = os.getenv("ENVIRON", "dev").lower()
    return DEFAULT_UPLOAD_URLS.get(environ, DEFAULT_UPLOAD_URLS["dev"]).rstrip("/")


ENVIRON = os.getenv("ENVIRON", "dev").lower()
HOST = get_host()
UPLOAD_HOST = get_upload_host()

logger.debug(f"[ENVIRON] Active environment: {ENVIRON}")
logger.debug(f"[HOST] Base URL: {HOST}")
logger.debug(f"[UPLOAD_HOST] CDN Upload URL: {UPLOAD_HOST}")
