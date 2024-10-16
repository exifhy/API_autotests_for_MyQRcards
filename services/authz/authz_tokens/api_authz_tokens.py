import os
import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.authz.authz_tokens.payloads import Payloads
from services.authz.authz_tokens.endpoints import Endpoints
from config.headers import Headers
from services.authz.authz_tokens.models.authz_tokens_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv


load_dotenv()
APP_ID = os.getenv('APP_ID')


class AuthzTokensAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Update JWT.")
    def post_update_jwt(self, access_token: str):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_update_jwt_endpoint,
            headers=self.headers.authorization_header(access_token, APP_ID)
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
        model = SuccessUpdateJwtResultModel(**response.json())
        logger.info(f'Successfully update JWT.')
        return model

