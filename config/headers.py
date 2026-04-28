import os


def _get_app_id() -> str | None:
    return os.getenv("APP_ID")


class Headers:
    basic_content_type = {
        "Content-Type": "application/json",
    }

    @staticmethod
    def authentication_header(token: str, app_id: str) -> dict:
        return {
            "Content-Type": "application/json",
            "X-APPLICATION-ID": app_id,
            "Accept": "application/json",
            "Authorization": f"Basic {token}",
            "Accept-Language": "ru-RU",
        }

    @staticmethod
    def authorization_header(bearer_token: str, app_id: str) -> dict:
        return {
            "Content-Type": "application/json",
            "X-APPLICATION-ID": app_id,
            "Accept": "application/json",
            "Authorization": f"Bearer {bearer_token}",
            "Accept-Language": "ru-RU",
        }

    @staticmethod
    def auth_header(bearer_token: str, app_id: str | None = None, **kwargs) -> dict:
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {bearer_token}",
            "X-APPLICATION-ID": app_id or _get_app_id(),
            **kwargs,
        }

    @staticmethod
    def without_authorization_field_header(app_id: str | None = None) -> dict:
        return {
            "Content-Type": "application/json",
            "X-APPLICATION-ID": app_id or _get_app_id(),
            "Accept": "application/json",
            "Accept-Language": "ru-RU",
        }
