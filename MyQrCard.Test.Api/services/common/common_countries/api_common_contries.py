import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.common.common_countries.payloads import Payloads
from services.common.common_countries.endpoints import Endpoints
from config.headers import Headers
from services.common.common_countries.models.common_countries_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class CommonCountriesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get list countries. Range: Items=1-5.")
    def get_list_countries_range_1_5(self):
        number = 5
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_countries_endpoint,
            headers=self.headers.basic_header_range(get_token(), number),
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list of countries.")
            return None
        assert response.status_code == HTTPStatus.PARTIAL_CONTENT, \
            (f'Expected status code {HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}, {data_response}')
        model = SuccessGetCountriesListResultModel(root=response.json())
        assert number == len(model.root), f'Expected {number} countries, bot got {len(model.root)}'
        logger.info(f'Successfully get list countries.')
        return model
