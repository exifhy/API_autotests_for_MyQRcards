import os
from dotenv import load_dotenv


load_dotenv()

APP_ID = os.getenv('APP_ID')
BASIC_TOKEN = os.getenv('SECOND_BASIC_TOKEN')


class Headers:

    basic_content_type = {
        "Content-Type": "application/json",
        # "X-APPLICATION-ID": "3"
    }

    authentication_fixture_header = {
        'Content-Type': 'application/json',
        'X-APPLICATION-ID': APP_ID,
        'Accept': 'application/json',
        'Authorization': f'Basic {BASIC_TOKEN}',
        'Accept-Language': 'ru-RU'
    }

    @staticmethod
    def basic_header(token: str) -> dict:
        basic = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            "Accept-Language": "ru-RU",
            "X-Application-ID": f"{APP_ID}",
            # "Range": "Items=1-25",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Content-Type": "application/json"
        }
        return basic

    @staticmethod
    def basic_header_with_range(token: str) -> dict:
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
    def upload_file_header(token: str, cont_type: str) -> dict:
        basic = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            'Origin': 'http://localhost:8080',
            "Accept-Language": "en-US",
            "X-Application-ID": f"{APP_ID}",
            'Content-Type': cont_type
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

    basic_header_without_authorization = {
        "Accept": "application/json",
        "Accept-Language": "ru-RU",
        "X-Application-ID": f"{APP_ID}",
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
    def auth_header(bearer_token: str, app_id: str, **kwargs) -> dict:
        header = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {bearer_token}',
            'X-APPLICATION-ID': app_id,
            **kwargs
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
