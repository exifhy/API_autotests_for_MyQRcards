import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.common.commont_measurement_units.payloads import Payloads
from services.common.commont_measurement_units.endpoints import Endpoints
from config.headers import Headers
from services.common.commont_measurement_units.models.common_measurement_units_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class CommonMeasurementUnitsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get list measurement units.")
    def get_list_measurement_units(self):
        number = 5
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_measurement_units_endpoint,
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
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list of measurement units.")
            return None
        assert response.status_code == HTTPStatus.PARTIAL_CONTENT, \
            (f'Expected status code {HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}, {data_response}')
        model = SuccessGetMeasurementUnitResultModel(root=response.json())
        assert number == len(model.root), f'Expected {number} measurement units, bot got {len(model.root)}'
        logger.info(f'Successfully get list measurement units.')
        return model
