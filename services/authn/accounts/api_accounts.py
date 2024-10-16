import os
import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.authn.accounts.payloads import Payloads
from services.authn.accounts.endpoints import Endpoints
from config.headers import Headers
from services.authn.accounts.models.accounts_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv


load_dotenv()

APP_ID = os.getenv('APP_ID')
BASIC_TOKEN = os.getenv('SECOND_BASIC_TOKEN')
USER_PHONE = os.getenv('USER_PHONE')


class AuthnAccountsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Account authentication by email address or username and password via Basic authorization.")
    def account_authentication_by_basic_authorization(self):
        start = time.time()
        response = requests.post(
            url=self.endpoints.account_authentication_by_basic_authorization_endpoint,
            headers=self.headers.authentication_header(BASIC_TOKEN, APP_ID)
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, f'{response.status_code}, {response.json()}'
        # assert model.expires_in == 1800, 'Cрок действия токена не равен 30 минутам'
        model = SuccessUserAccountAuthenticationModel(**response.json())
        logger.info(f'Successfully receiving the {model.access_token}.')
        return model

    @allure.step("Authentication with invalid TOKEN.")
    def account_authentication_with_invalid_token(self):
        basic_token = "VeryWrong.InvalidTokEn"
        start = time.time()
        response = requests.post(
            url=self.endpoints.account_authentication_by_basic_authorization_endpoint,
            headers=self.headers.authentication_header(basic_token, APP_ID)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.UNAUTHORIZED, f'{response.status_code}, {response.json()}'
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].code == "AccountNotFound", "Unexpected Response Code for Invalid Token"
        logger.info(f'Expected error: {model.list_model[0].code}.')
        return model

    @allure.step("Request without Authorization header.")
    def request_without_authorization_header(self):
        start = time.time()
        response = requests.post(
            url=self.endpoints.account_authentication_by_basic_authorization_endpoint,
            headers=self.headers.without_authorization_field_header(APP_ID)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CONFLICT, f'{response.status_code}, {response.json()}'
        model = ErrorModel(list_model=response.json())
        logger.info(f'Expected error: {model.list_model[0].code}.')
        return model

    @allure.step("Account authentication by sso.")
    def post_account_authentication_by_sso(self, token: str):
        start = time.time()
        response = requests.post(
            url=self.endpoints.account_authentication_by_sso_endpoint,
            headers=self.headers.authentication_header(token, APP_ID)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, f'{response.status_code}, {response.json()}'
        model = SuccessUserAccountAuthenticationModel(**response.json())
        logger.info(f'Successful account authentication by sso.')
        return model

    @allure.step("Generating code for authorization by SMS.")
    def post_generating_code_for_authorization_by_sms(self):
        start = time.time()
        response = requests.post(
            url=self.endpoints.generating_code_for_authorization_by_sms_endpoint,
            headers=self.headers.without_authorization_field_header(APP_ID),
            json=self.payloads.accounts_sms_send_payload(USER_PHONE)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        if response.status_code == HTTPStatus.UNAUTHORIZED:
            logger.error(f'Status code:{response.status_code}, body: {response.json()}')
        else:
            assert response.status_code == HTTPStatus.OK, f'{response.status_code}, {response.json()}'
            logger.info(f'Successful generating code for authorization by SMS.')

    @allure.step("Generating code for authorization via SMS with invalid phone number(00123456456342)")
    def post_generating_code_for_authorization_by_sms_with_invalid_phone_len(self):
        start = time.time()
        response = requests.post(
            url=self.endpoints.generating_code_for_authorization_by_sms_endpoint,
            headers=self.headers.without_authorization_field_header(APP_ID),
            json=self.payloads.accounts_sms_send_payload("00123456456")
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.NOT_FOUND, f'{response.status_code}, {response.json()}'
        model = ErrorModel(list_model=response.json())
        logger.info(f'Expected error: {model.list_model[0].message}.')
        return model

    @allure.step("Generating code for authorization via SMS with invalid phone number(abcadsfqwer)")
    def post_generating_code_for_authorization_by_sms_with_invalid_phone_abc(self):
        start = time.time()
        response = requests.post(
            url=self.endpoints.generating_code_for_authorization_by_sms_endpoint,
            headers=self.headers.without_authorization_field_header(APP_ID),
            json=self.payloads.accounts_sms_send_payload("abcadsfqwer")
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.BAD_REQUEST, f'{response.status_code}, {response.json()}'
        model = ErrorModel(list_model=response.json())
        logger.info(f'Expected error: {model.list_model[0].message}.')
        return model

    @allure.step("SMS code verification.")
    def post_sms_code_verification(self, code):
        start = time.time()
        response = requests.post(
            url=self.endpoints.check_sms_code_endpoint,
            headers=self.headers.without_authorization_field_header(APP_ID),
            json=self.payloads.accounts_sms_login_payload(
                code=code,
                phone=USER_PHONE
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.OK, f'Status code {response.status_code}, {response.json()}'
        model = SuccessUserAccountAuthenticationModel(**response.json())
        logger.info(f'Successful SMS code verification.')
        return model
