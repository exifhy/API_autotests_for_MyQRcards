import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.auth.auth_verification_codes.payloads import Payloads
from services.auth.auth_verification_codes.endpoints import Endpoints
from config.headers import Headers
from services.auth.auth_verification_codes.models.auth_verification_codes_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os

load_dotenv()
APP_ID = os.getenv('APP_ID')


class AuthVerificationCodesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Checks the verification code.")
    def post_checks_verification_code(self, params, token: str):
        start = time.time()
        response = requests.post(
            url=self.endpoints.check_verification_codes_endpoint,
            headers=self.headers.auth_header(bearer_token=token, app_id=APP_ID),
            json=self.payloads.check_verification_codes_payload(**params)
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
        assert response.status_code == HTTPStatus.OK, f'{response.status_code}, {response.json()}'
        logger.warning(f'Successfully checks the verification code.')
