import os

from loguru import logger


SUPPORTED_ENVS = ("dev", "prod")


def get_host() -> str:
    environ = os.getenv("ENVIRON", "dev").lower()
    if environ not in SUPPORTED_ENVS:
        raise ValueError(f"Unsupported environment: {environ}")

    host = (
        os.getenv("HOST")
        or os.getenv(f"URL_{environ.upper()}_API")
    )
    if not host:
        raise ValueError(
            f"HOST is not configured for environment '{environ}'. "
            f"Set HOST or URL_{environ.upper()}_API, or add 'host' to data/ids.{environ}.json"
        )
    return host.rstrip("/")


ENVIRON = os.getenv("ENVIRON", "dev").lower()
HOST = get_host()

logger.debug(f"[ENVIRON] Active environment: {ENVIRON}")
logger.debug(f"[HOST] Base URL: {HOST}")
