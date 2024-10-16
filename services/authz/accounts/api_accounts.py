import os
import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.authz.accounts.payloads import Payloads
from services.authz.accounts.endpoints import Endpoints
from config.headers import Headers
from services.authz.accounts.models.accounts_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv


load_dotenv()
APP_ID = os.getenv('APP_ID')
TENANT_ID = os.getenv('TENANT_ID')
TENANT_MEMBER_ID = os.getenv('TENANT_MEMBER_ID')


class AuthzAccountsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Authorization of a tenant account.")
    def account_authorization_of_tenant_account(self, bearer_token):
        start = time.time()
        response = requests.post(
            url=self.endpoints.authorization_endpoint,
            headers=self.headers.authorization_header(bearer_token, APP_ID),
            json=self.payloads.authorization_payloads(TENANT_ID, TENANT_MEMBER_ID)
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
        model = SuccessAuthorizationModel(**response.json())
        logger.info(f'Successfully receiving the Bearer token.')
        return model

    @allure.step("Authorization of a tenant account without tenantMemberID field in the payload.")
    def account_authorization_of_tenant_account_without_member_id_in_body(self, bearer_token):
        start = time.time()
        response = requests.post(
            url=self.endpoints.authorization_endpoint,
            headers=self.headers.authorization_header(bearer_token, APP_ID),
            json=self.payloads.authorization_without_tenant_member_id_payloads(TENANT_ID)
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
        assert response.status_code == HTTPStatus.CONFLICT, f'{response.status_code}, {response.json()}'
        model = ErrorModel(list_model=response.json())
        logger.info(f'Expected error: {model.list_model[0].code}.')
        return model

    @allure.step("Authorization of a tenant account without tenantID field in the payload.")
    def account_authorization_of_tenant_account_without_tenant_id_in_body(self, bearer_token):
        start = time.time()
        response = requests.post(
            url=self.endpoints.authorization_endpoint,
            headers=self.headers.authorization_header(bearer_token, APP_ID),
            json=self.payloads.authorization_without_tenant_id_payloads(TENANT_MEMBER_ID)
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
        assert response.status_code == HTTPStatus.CONFLICT, f'{response.status_code}, {response.json()}'
        model = ErrorModel(list_model=response.json())
        logger.info(f'Expected error: {model.list_model[0].code}.')
        return model
