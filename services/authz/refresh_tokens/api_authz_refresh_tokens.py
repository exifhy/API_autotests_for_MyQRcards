import os
import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.authz.refresh_tokens.payloads import Payloads
from services.authz.refresh_tokens.endpoints import Endpoints
from config.headers import Headers
from services.authz.refresh_tokens.models.authz_refresh_tokens_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv


load_dotenv()
APP_ID = os.getenv('APP_ID')


class AuthzRefreshTokensAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Returns the refresh token with default parameters.")
    def get_refresh_token_with_default_parameters(self, access_token: str):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_refresh_token_with_default_parameters_endpoint,
            headers=self.headers.authorization_header(access_token, APP_ID),
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
        model = SuccessUpdateRefreshJwtResultBaseModel(**response.json())
        logger.info(f'Successfully returns the refresh token with default parameters.')
        return model

    @allure.step("Generates an refresh token and returns it.")
    def post_generates_and_returns_refresh_token(self, access_token: str):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_generates_and_returns_refresh_token_endpoint,
            headers=self.headers.authorization_header(access_token, APP_ID),
            json=self.payloads.generates_and_returns_refresh_token_payload
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
        assert response.status_code == HTTPStatus.OK, f'{response.status_code}, {response.json()}'
        model = SuccessUpdateRefreshJwtResultBaseModel(**response.json())
        logger.info(f'Successfully generates an refresh token and returns it.')
        return model
