import os
from dotenv import load_dotenv

load_dotenv()


class Headers:

    basic_content_type = {
        "Content-Type": "application/json"
    }

    basic = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('API_TOKEN')}"
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
