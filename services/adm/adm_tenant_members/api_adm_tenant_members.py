import os
import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.adm.adm_tenant_members.payloads import Payloads
from services.adm.adm_tenant_members.endpoints import Endpoints
from config.headers import Headers
from services.adm.adm_tenant_members.models.adm_tenant_members_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token
from dotenv import load_dotenv


load_dotenv()
APP_ID = os.getenv('APP_ID')


class AdmTenantMembersAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Marks the tenant member as deleted.")
    def delete_tenant_member_by_id(self, tenant_member_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_tenant_member_by_id_endpoint(tenant_member_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, f'{response.status_code}, {response.json()}'
        logger.info(f'Successfully marks the tenant member as deleted.')

    @allure.step("Returns the API user in the current tenant.")
    def get_returns_api_user_in_current_tenant(self, access_token: str):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_returns_api_user_in_current_tenant_endpoint,
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
        model = SuccessTenantMembersListResultModel(**response.json())
        logger.info(f'Successfully returns the API user in the current tenant.')
        return model

    @allure.step("Get API user in the current tenant.")
    def get_api_user_in_current_tenant(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_returns_api_user_in_current_tenant_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessTenantMembersListResultModel(**response.json())
        logger.info(f'Successfully get API user in the current tenant.')
        return model
