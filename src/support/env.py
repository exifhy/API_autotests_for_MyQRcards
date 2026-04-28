import os


def get_env(name: str, default=None):
    return os.getenv(name, default)


def get_api_user_token():
    return get_env("API_USER_TOKEN")


def get_power_user_token():
    return get_env("POWER_USER_TOKEN")


def get_tenant_owner_token():
    return get_env("SECOND_BASIC_TOKEN")


def get_tenant_id():
    return get_env("TENANT_ID")
