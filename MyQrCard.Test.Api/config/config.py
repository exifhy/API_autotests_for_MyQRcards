import os
from loguru import logger

ENVIRON = os.getenv("ENVIRON", "dev").lower()

URLS = {
    "dev": os.getenv("URL_DEV_HUBEX"),
    "stage": os.getenv("URL_STAGE_HUBEX"),
    "prod": os.getenv("URL_PROD_HUBEX"),
}

if ENVIRON not in URLS or not URLS[ENVIRON]:
    raise ValueError(f"Invalid or missing URL for environment: {ENVIRON}")

HOST = URLS[ENVIRON]

logger.debug(f"[ENVIRON] Active environment: {ENVIRON}")
logger.debug(f"[HOST] Base URL: {HOST}")
