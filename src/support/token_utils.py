import os


def get_token() -> str | None:
    return os.getenv("API_TOKEN") or os.getenv("LK_JWT")
