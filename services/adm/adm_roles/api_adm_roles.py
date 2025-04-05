import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.adm.adm_roles.payloads import Payloads
from services.adm.adm_roles.endpoints import Endpoints
from config.headers import Headers
from services.adm.adm_roles.models.adm_roles_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class AdmUserRolesAPI(Helper):

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
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, f'{response.status_code}, {response.json()}'
        logger.info(f'Successfully get list roles for tenant.')
