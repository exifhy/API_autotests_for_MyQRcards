import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.adm.adm_ban_reasons.payloads import Payloads
from services.adm.adm_ban_reasons.endpoints import Endpoints
from config.headers import Headers
from services.adm.adm_ban_reasons.models.adm_ban_reasons_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class AdmBanReasonsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get list ban reasons.")
    def get_list_ban_reasons(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_ban_reasons_endpoint,
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list of ban reasons.")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}, {data_response}')
        model = SuccessGetBanReasonsListResultModel(root=response.json())
        logger.info(f'Successfully get list ban reasons.')
        return model
