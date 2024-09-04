import os
from dotenv import load_dotenv


load_dotenv()

APP_ID = os.getenv('APP_ID')


class Headers:

    basic_content_type = {
        "Content-Type": "application/json"
    }

    @staticmethod
    def basic_header(token: str) -> dict:
        basic = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            "Accept-Language": "ru-RU",
            "X-Application-ID": f"{APP_ID}",
            "Range": "Items=1-25",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Content-Type": "application/json"
        }
        return basic

    @staticmethod
    def export_header(token: str) -> dict:
        basic = {
            "Accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "Authorization": f"Bearer {token}",
            "Accept-Language": "ru-RU",
            "X-Application-ID": f"{APP_ID}",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Connection": "keep-alive"
        }
        return basic

    basic = {
        "Accept": "application/json",
        "Authorization": f"Bearer",
        "Accept-Language": "ru - RU",
        "X-Application-ID": f"{APP_ID}",
        "Range": "Items=1-25",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Content-Type": "application/json"
    }

    @staticmethod
    def authentication_header(token: str, app_id: str) -> dict:
        header = {
            'Content-Type': 'application/json',
            'X-APPLICATION-ID': app_id,
            'Accept': 'application/json',
            'Authorization': f'Basic {token}',
            'Accept-Language': 'ru-RU',
        }
        return header

    @staticmethod
    def authorization_header(bearer_token: str, app_id: str) -> dict:
        header = {
            'Content-Type': 'application/json',
            'X-APPLICATION-ID': app_id,
            'Accept': 'application/json',
            'Authorization': f'Bearer {bearer_token}',
            'Accept-Language': 'ru-RU',
        }
        return header

    @staticmethod
    def without_authorization_field_header(app_id: str) -> dict:
        header = {
            'Content-Type': 'application/json',
            'X-APPLICATION-ID': app_id,
            'Accept': 'application/json',
            'Accept-Language': 'ru-RU'
        }
        return header
