import os
import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.authz.accounts.payloads import Payloads
from services.authz.accounts.endpoints import Endpoints
from config.headers import Headers
from services.authz.accounts.models.accounts_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv


load_dotenv()


class AuthzAccountsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Authorisation of a tenant account.")
    def account_authorisation_of_tenant_account(self, bearer_token):
        app_id = os.getenv('APP_ID')
        tenant_id = os.getenv('TENANT_ID')
        member_id = os.getenv('TENANT_MEMBER_ID')
        start = time.time()
        response = requests.post(
            url=self.endpoints.authorisation_endpoint,
            headers=self.headers.authorization_header(bearer_token, app_id),
            json=self.payloads.authorization_payloads(tenant_id, member_id)
        )
        end = time.time()
        assert response.status_code == HTTPStatus.OK, response.json()
        logger.info(response.headers)
        self.attach_response(response.json())
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        model = SuccessAuthorizationModel(**response.json())
        logger.info(f'Successfully receiving the Bearer token.')
        return model

    @allure.step("Authorisation of a tenant account without tenantMemberID field in the payload.")
    def account_authorisation_of_tenant_account_without_member_id_in_body(self, bearer_token):
        app_id = os.getenv('APP_ID')
        tenant_id = os.getenv('TENANT_ID')
        start = time.time()
        response = requests.post(
            url=self.endpoints.authorisation_endpoint,
            headers=self.headers.authorization_header(bearer_token, app_id),
            json=self.payloads.authorization_without_tenant_member_id_payloads(tenant_id)
        )
        end = time.time()
        logger.info(response.json())
        logger.info(response.status_code)
        logger.info(response.headers)
        assert response.status_code == HTTPStatus.CONFLICT, response.json()
        self.attach_response(response.json())
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        model = ErrorModel(list_model=response.json())
        logger.info(f'Expected error: {model.list_model[0].code}.')
        return model

    @allure.step("Authorisation of a tenant account without tenantID field in the payload.")
    def account_authorisation_of_tenant_account_without_tenant_id_in_body(self, bearer_token):
        app_id = os.getenv('APP_ID')
        member_id = os.getenv('TENANT_MEMBER_ID')
        start = time.time()
        response = requests.post(
            url=self.endpoints.authorisation_endpoint,
            headers=self.headers.authorization_header(bearer_token, app_id),
            json=self.payloads.authorization_without_tenant_id_payloads(member_id)
        )
        end = time.time()
        logger.info(response.json())
        assert response.status_code == HTTPStatus.CONFLICT, response.json()
        logger.info(response.headers)
        self.attach_response(response.json())
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        model = ErrorModel(list_model=response.json())
        logger.info(f'Expected error: {model.list_model[0].code}.')
        return model
