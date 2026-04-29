from dotenv import load_dotenv
import os


def get_env(name: str, default=None):
    load_dotenv()
    return os.getenv(name, default)


def get_api_user_token():
    return get_env("API_USER_TOKEN")


def get_power_user_token():
    return get_env("POWER_USER_TOKEN")


def get_tenant_owner_token():
    return get_env("SECOND_BASIC_TOKEN")


def get_tenant_id():
    return get_env("TENANT_ID")


def get_app_id():
    return get_env("APP_ID")
