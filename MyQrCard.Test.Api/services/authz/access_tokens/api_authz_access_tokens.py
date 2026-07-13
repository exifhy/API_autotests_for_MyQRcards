import os
import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.authz.access_tokens.payloads import Payloads
from services.authz.access_tokens.endpoints import Endpoints
from config.headers import Headers
from services.authz.access_tokens.models.authz_access_tokens_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv


load_dotenv()
APP_ID = os.getenv('APP_ID')


class AuthzAccessTokensAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Updates the resource access token.")
    def post_updates_resource_access_token(self, access_token: str, refresh_token: str):
        start = time.time()
        response = requests.post(
            url=self.endpoints.updates_resource_access_token_endpoint,
            headers=self.headers.authorization_header(access_token, APP_ID),
            json=self.payloads.updates_resource_access_token_payload(access_token, refresh_token)
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
        assert response.status_code == HTTPStatus.OK, f'{response.status_code}, {response.json()}'
        model = SuccessUpdateJwtResultBaseModel(**response.json())
        assert refresh_token != model.refresh_token, f"Token has not been updated."
        logger.info(f'Successfully updates the resource access token.')
        return model
