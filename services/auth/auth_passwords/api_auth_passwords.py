import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.auth.auth_passwords.payloads import Payloads
from services.auth.auth_passwords.endpoints import Endpoints
from config.headers import Headers
from services.auth.auth_passwords.models.auth_passwords_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
APP_ID = os.getenv('APP_ID')


class AuthPasswordsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Changes the account password.")
    def post_change_password(self, params):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_change_passwords_endpoint,
            headers=self.headers.auth_header(bearer_token=API_TOKEN, app_id=APP_ID),
            json=self.payloads.change_password_payload(**params)
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
        assert response.status_code == HTTPStatus.OK, f'Status code {response.status_code}'
        logger.warning(f'Successfully changes the account password.')
