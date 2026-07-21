import os


def get_token() -> str | None:
    return os.getenv("API_TOKEN") or os.getenv("LK_JWT")


def get_expired_jwt() -> str | None:
    return os.getenv("EXPIRED_JWT")


def get_test_jwt() -> str | None:
    return os.getenv("TEST_LK_JWT")


def get_manager_password() -> str | None:
    return os.getenv("MANAGER_PASSWORD")


def get_manager_jwt() -> str | None:
    """REQUIREMENT 29760 (Manager API). TEST_LK_JWT is the JWT of the account
    (ermolin.ds@hubex.ru) that was manually granted manager rights in the DB —
    the only account that currently passes /Manager/* auth. Regular LK_JWT is
    NOT a manager and never will be for this account."""
    return os.getenv("TEST_LK_JWT")
