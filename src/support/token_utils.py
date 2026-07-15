import os


def get_token() -> str | None:
    return os.getenv("API_TOKEN") or os.getenv("LK_JWT")


def get_expired_jwt() -> str | None:
    return os.getenv("EXPIRED_JWT")


def get_test_jwt() -> str | None:
    return os.getenv("TEST_LK_JWT")
