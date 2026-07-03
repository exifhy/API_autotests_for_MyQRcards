import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.common.common_time_zones.payloads import Payloads
from services.common.common_time_zones.endpoints import Endpoints
from config.headers import Headers
from services.common.common_time_zones.models.common_time_zones_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class CommonTimeZonesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get list time zones.")
    def get_list_time_zones(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_time_zones_endpoint,
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
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list of tags.")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}, {data_response}')
        model = SuccessGetTimeZonesListResultsModel(root=response.json())
        logger.info(f'Successfully get list time zones.')
        return model

    @allure.step("Get time zone info by timezoneId.")
    def get_time_zone_info_by_timezone_id(self, model_timezones):
        timezone_id = next(iter(model_timezones.root))
        param = {
            "timezoneId": timezone_id
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_time_zones_info_endpoint, params=param,
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
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no time zone info.")
            return None
        assert response.status_code == HTTPStatus.OK, \
            (f'Expected status code {HTTPStatus.OK}, '
             f'but got {response.status_code}, {data_response}')
        model = TimeZonesInfoListResultsModel(**response.json())
        logger.info(f'Successfully get timezones info by timezone_id {timezone_id}.')
        return model
