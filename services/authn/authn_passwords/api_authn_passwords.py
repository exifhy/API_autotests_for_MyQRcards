import os
import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.authn.authn_passwords.payloads import Payloads
from services.authn.authn_passwords.endpoints import Endpoints
from config.headers import Headers
from services.authn.authn_passwords.models.authn_passwords_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv


load_dotenv()

APP_ID = os.getenv('APP_ID')
BASIC_TOKEN = os.getenv('SECOND_BASIC_TOKEN')
USER_PHONE = os.getenv('USER_PHONE')


class AuthnPasswordsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Sets the password for the newly created account.")
    def post_sets_password_for_new_account(self, params):
        start = time.time()
        response = requests.post(
            url=self.endpoints.sets_password_for_new_account_endpoint,
            headers=self.headers.without_authorization_field_header(APP_ID),
            json=self.payloads.password_set_payload(**params)
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        assert response.status_code == HTTPStatus.ACCEPTED, response.status_code
        model = SuccessAccountJwtResultBase(**response.json())
        logger.info(f'Successfully sets the password for the newly created account.')
        return model
