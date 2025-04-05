import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.adm.adm_tenants.payloads import Payloads
from services.adm.adm_tenants.endpoints import Endpoints
from config.headers import Headers
from services.adm.adm_tenants.models.adm_tenants_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class AdmTenantsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get data current tenant.")
    def get_data_current_tenant(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_data_current_tenant_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, f'Status code {response.status_code}, {response.json()}'
        model = SuccessGetCurrentTenantResult(**response.json())
        logger.info(f'Successfully get data current tenant.')
        return model
