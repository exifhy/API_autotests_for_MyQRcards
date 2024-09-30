import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.auth.auth_messages.payloads import Payloads
from services.auth.auth_messages.endpoints import Endpoints
from config.headers import Headers
from services.auth.auth_messages.models.auth_messages_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
APP_ID = os.getenv('APP_ID')
USER_EMAIL = os.getenv('USER_EMAIL')


class AuthMessagesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Sends a mail verification e-mail to the specified e-mail address "
                 "(if not specified, to the account address).")
    def post_message_verify_email(self, account_id: int, email: str, token: str):
        params = {
            "email": email
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_message_verify_email_endpoint,
            headers=self.headers.auth_header(bearer_token=token, app_id=APP_ID),
            json=self.payloads.messages_verify_payloads(account_id, **params)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_url(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}'
        model = AccountsVerificationResult(**response.json())
        logger.warning(f'Successfully sends a mail verification email to the specified email address.')
        return model

    @allure.step("Sends SMS of mail phone number verification to the specified phone number "
                 "(if not specified, to the account phone number).")
    def post_message_verify_phone(self, account_id: int, phone: str, token: str):
        params = {
            "phone": phone
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_message_verify_phone_endpoint,
            headers=self.headers.auth_header(bearer_token=token, app_id=APP_ID),
            json=self.payloads.messages_verify_payloads(account_id, **params)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_url(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}'
        model = AccountsVerificationResult(**response.json())
        logger.warning(f'Successfully sends SMS of mail phone number verification to the specified phone number.')
        return model

    @allure.step("Sends a password change request to the specified e-mail address, "
                 "for authenticated user - to the account e-mail address.")
    def post_message_request_password_change(self, token: str, email: str):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_message_request_password_change_endpoint,
            headers=self.headers.auth_header(bearer_token=token, app_id=APP_ID),
            json=self.payloads.request_password_change(value=email)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_url(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}'
        model = AccountsVerificationResult(**response.json())
        logger.warning(f'Successfully sends a password change request to the specified e-mail address.')
        return model
