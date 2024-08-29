import os
import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.authn.accounts.payloads import Payloads
from services.authn.accounts.endpoints import Endpoints
from config.headers import Headers
from services.authn.accounts.models.accounts_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv


load_dotenv()


class AuthnAccountsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Account authentication by email address or username and password via Basic authorisation.")
    def account_authentication_by_basic_authorisation(self):
        basic_token = os.getenv('SECOND_BASIC_TOKEN')
        app_id = os.getenv('APP_ID')
        start = time.time()
        response = requests.post(
            url=self.endpoints.account_authentication_by_basic_authorisation_endpoint,
            headers=self.headers.authentication_header(basic_token, app_id)
        )
        end = time.time()
        # logger.info(response.request.headers)
        assert response.status_code == HTTPStatus.OK, response.json()
        # assert model.expires_in == 1800, 'Cрок действия токена не равен 30 минутам'
        self.attach_response(response.json())
        self.attach_time(start, end)
        model = SuccessUserAccountAuthenticationModel(**response.json())
        logger.info(f'Successfully receiving the {model.access_token}.')
        return model

    @allure.step("Authentication with invalid TOKEN.")
    def account_authentication_with_invalid_token(self):
        basic_token = "VeryWrong.InvalidTokEn"
        app_id = os.getenv('APP_ID')
        start = time.time()
        response = requests.post(
            url=self.endpoints.account_authentication_by_basic_authorisation_endpoint,
            headers=self.headers.authentication_header(basic_token, app_id)
        )
        end = time.time()
        # logger.info(response.request.headers)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, response.json()
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].code == "AccountNotFound", "Unexpected Response Code for Invalid Token"
        self.attach_time(start, end)
        self.attach_response(response.json())
        logger.info(f'Expected error: {model.list_model[0].code}.')
        return model

    @allure.step("Request without Authorization header.")
    def request_without_authorization_header(self):
        app_id = os.getenv('APP_ID')
        start = time.time()
        response = requests.post(
            url=self.endpoints.account_authentication_by_basic_authorisation_endpoint,
            headers=self.headers.without_authorization_field_header(app_id)
        )
        end = time.time()
        # logger.info(response.request.headers)
        assert response.status_code == HTTPStatus.CONFLICT, response.json()
        self.attach_response(response.json())
        self.attach_time(start, end)
        model = ErrorModel(list_model=response.json())
        logger.info(f'Expected error: {model.list_model[0].code}.')
        return model
