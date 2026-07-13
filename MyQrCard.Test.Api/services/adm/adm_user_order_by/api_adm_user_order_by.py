import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.adm.adm_user_order_by.payloads import Payloads
from services.adm.adm_user_order_by.endpoints import Endpoints
from config.headers import Headers
from services.adm.adm_user_order_by.models.adm_user_order_by_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class AdmUserOrderByAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get list user order by.")
    def get_list_user_order_by(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_user_order_by_endpoint,
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
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list of user order by.")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}, {data_response}')
        model = UserOrderByListResponseModel(root=response.json())
        logger.info(f'Successfully Get list user order by.')
        return model
