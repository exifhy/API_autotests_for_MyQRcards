import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.adm.adm_tenant_settings.payloads import Payloads
from services.adm.adm_tenant_settings.endpoints import Endpoints
from config.headers import Headers
from services.adm.adm_tenant_settings.models.adm_tenant_settings_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class AdmTenantSettingsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get tenant settings.")
    def get_tenant_settings(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_tenant_settings_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no tenant settings.")
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = TenantSettingsGetResultModel(**response.json())
        logger.info(f'Successfully get tenant settings.')
        return model

    @allure.step("Get tenant settings without Authorization.")
    def get_tenant_settings_without_authorization(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_tenant_settings_endpoint,
            headers=self.headers.basic_header_without_authorization
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, \
            f'Expected status code {HTTPStatus.UNAUTHORIZED}, but got {response.status_code}, {data_response}'
        logger.warning(f'Expected result: error {response.status_code}, message: Unauthorized')
        return None
