import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.sla.sla_criticalities.payloads import Payloads
from services.sla.sla_criticalities.endpoints import Endpoints
from config.headers import Headers
from services.sla.sla_criticalities.models.sla_criticalities_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class SlaCriticalitiesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get list criticalities and returns ID the first existing.")
    def get_list_criticalities_return_first_id(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_criticalities_endpoint,
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
        model = SuccessGetListCriticalitiesModel(root=response.json())
        for key, value in model.root.items():
            logger.info(f'Successfully get list criticalities.')
            logger.info(f'Criticality ID: {key}, name: {value.name}')
            return key

    @allure.step("Get list criticalities.")
    def get_list_criticalities(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_criticalities_endpoint,
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
        model = SuccessGetListCriticalitiesModel(root=response.json())
        logger.info(f'Successfully get list a criticalities.')
        return model
