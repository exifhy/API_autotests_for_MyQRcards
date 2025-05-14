import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.adm.adm_roles.payloads import Payloads
from services.adm.adm_roles.endpoints import Endpoints
from config.headers import Headers
from services.adm.adm_roles.models.adm_roles_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class AdmRolesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get list roles for tenant.")
    def get_list_roles(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_roles_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessGetListRolesModel(results=response.json())
        logger.info(f'Successfully get list roles for tenant.')
        return model
