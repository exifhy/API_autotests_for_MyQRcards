import os
import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.authz.service_tokens.payloads import Payloads
from services.authz.service_tokens.endpoints import Endpoints
from config.headers import Headers
from services.authz.service_tokens.models.authz_service_tokens_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv


load_dotenv()
APP_ID = os.getenv('APP_ID')


class AuthzServiceTokensAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Generates a new api user access token and returns it.")
    def post_user_api_token_generation(self, access_token: str, user_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_user_api_token_generation_endpoint,
            headers=self.headers.authorization_header(access_token, APP_ID),
            json=self.payloads.api_token_payload(user_id)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, f'{response.status_code}, {response.json()}'
        model = SuccessGenerateServiceTokenModel(result=response.json())
        logger.info(f'Successfully generates a new api user access token and returns it.')
        return model

    @allure.step("Deletes the api user access token.")
    def delete_user_api_token(self, access_token: str, user_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_user_api_token_endpoint,
            headers=self.headers.authorization_header(access_token, APP_ID),
            json=self.payloads.api_token_payload(user_id)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, f'{response.status_code}, {response.json()}'
        logger.info(f'Successfully deletes the api user access token.')
