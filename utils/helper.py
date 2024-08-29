import base64
import urllib.parse
import allure
import json
from allure_commons.types import AttachmentType


class Helper:

    @classmethod
    def attach_response(cls, response):
        response = json.dumps(response, indent=4, ensure_ascii=False)
        allure.attach(body=response.encode('utf-8'), name='API Response', attachment_type=AttachmentType.JSON)

    @classmethod
    def attach_request(cls, request):
        if isinstance(request, bytes):
            request = request.decode('utf-8')
        request_obj = json.loads(request)
        readable_request = json.dumps(request_obj, ensure_ascii=False, indent=2)
        allure.attach(body=readable_request, name='API Request body', attachment_type=AttachmentType.JSON)

    @classmethod
    def attach_time(cls, start_time, end_time):
        response_time_ms = (end_time - start_time) * 1000
        allure.attach(f'API Response time: {response_time_ms:.2f}ms', name="Response Time",
                      attachment_type=AttachmentType.JSON)

    @staticmethod
    def basic_token_generation(login: str, password: str) -> str:

        encoded_login = urllib.parse.quote(login, safe='')
        encoded_password = urllib.parse.quote(password, safe='')

        # Формируем строку логин:пароль
        credentials = f"{encoded_login}:{encoded_password}"

        # Кодируем строку в base64
        encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

        return encoded_credentials

    @staticmethod
    def build_url(base_url: str, params: dict) -> str:
        query_string = urllib.parse.urlencode(params)
        full_url = f"{base_url}/?{query_string}"
        return full_url
