import base64
import urllib.parse
import allure
import json
from allure_commons.types import AttachmentType
from requests.structures import CaseInsensitiveDict
from loguru import logger


class Helper:

    @classmethod
    def attach_response(cls, response):
        response = json.dumps(response, indent=4, ensure_ascii=False)
        allure.attach(body=response.encode('utf-8'), name='API Response', attachment_type=AttachmentType.JSON)

    @classmethod
    def attach_response_headers(cls, response):
        if isinstance(response, CaseInsensitiveDict):
            response = dict(response)
        response = json.dumps(response, indent=4, ensure_ascii=False)
        allure.attach(body=response.encode('utf-8'), name='API Response headers', attachment_type=AttachmentType.JSON)

    @classmethod
    def attach_request(cls, request):
        if isinstance(request, bytes):
            request = request.decode('utf-8')
        request_obj = json.loads(request)
        readable_request = json.dumps(request_obj, ensure_ascii=False, indent=2)
        allure.attach(body=readable_request, name='API Request body', attachment_type=AttachmentType.JSON)

    @classmethod
    def attach_url(cls, request):
        if isinstance(request, bytes):
            request = request.decode('utf-8')
        allure.attach(body=request, name='Service API url', attachment_type=AttachmentType.TEXT)

    @classmethod
    def attach_token(cls, request):
        if isinstance(request, bytes):
            request = request.decode('utf-8')
        allure.attach(body=request, name='Token', attachment_type=AttachmentType.TEXT)

    @classmethod
    def attach_request_txt(cls, request):
        if isinstance(request, bytes):
            request = request.decode('utf-8')
        allure.attach(body=request, name='API Request body', attachment_type=AttachmentType.TEXT)

    @classmethod
    def attach_time(cls, start_time, end_time):
        response_time_ms = (end_time - start_time) * 1000
        allure.attach(f'API Response time: {response_time_ms:.2f}ms', name="Response Time",
                      attachment_type=AttachmentType.JSON)

    @classmethod
    def attach_token_expiration_time(cls, token_expiration_time):
        """Добавляет время истечения токена в отчет Allure."""
        expiration_str = token_expiration_time.strftime('%Y-%m-%d %H:%M:%S %Z')
        allure.attach(f'Token Expiration Time: {expiration_str}',
                      name="Token Expiration",
                      attachment_type=allure.attachment_type.TEXT)

    @classmethod
    def attach_test_start_time(cls, test_start_time):
        """Добавляет время начала теста в отчет Allure."""
        expiration_str = test_start_time.strftime('%Y-%m-%d %H:%M:%S %Z')
        allure.attach(f'Test start time: {expiration_str}',
                      name="Start time",
                      attachment_type=allure.attachment_type.TEXT)

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

    @staticmethod
    def response_content(response) -> str:

        allure.attach(body=str(response.request.method), name='Method', attachment_type=AttachmentType.TEXT)

        allure.attach(body=str(response.status_code), name='Status code', attachment_type=AttachmentType.TEXT)

        if response.content:
            return response.json()
        else:
            return "The response body is empty."

    @staticmethod
    def assert_already_done(response, model) -> None:
        assert model.list_model[0].code == "AlreadyDone", \
            f'Expected <AlreadyDone>, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "Операция была выполнена ранее", \
            f'Expected <Операция была выполнена ранее>, but got {model.list_model[0].message}'
        assert "AlreadyDone" in response.headers["X-Application-Errors"], \
            f'Expected <AlreadyDone>, but got {response.headers["X-Application-Errors"]}'
        return None

    @staticmethod
    def assert_receipt_not_found(response, model) -> None:
        assert model.list_model[0].code == "ReceiptNotFound", \
            f'Expected <ReceiptNotFound>, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "Документ оприходывания не найден", \
            f'Expected <Документ оприходывания не найден>, but got {model.list_model[0].message}'
        assert "ReceiptNotFound" in response.headers["X-Application-Errors"], \
            f'Expected <ReceiptNotFound>, but got {response.headers["X-Application-Errors"]}'
        return None
