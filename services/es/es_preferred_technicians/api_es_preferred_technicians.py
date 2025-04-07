import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.es.es_preferred_technicians.payloads import Payloads
from services.es.es_preferred_technicians.endpoints import Endpoints
from config.headers import Headers
from services.es.es_preferred_technicians.models.es_preferred_technicians_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class EsPreferredTechniciansAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Adding a preferred technicians for an asset.")
    def post_add_preferred_technicians(self, asset_id: int, *user_ids: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_preferred_technicians_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_preferred_technicians_payload(
                asset_id,
                *user_ids
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, f'{response.status_code}, {response.json()}'
        logger.info(f'Successfully add preferred technicians with IDs: {user_ids} for an asset with ID: {asset_id}.')

    @allure.step("Get preferred technicians from asset by id.")
    def get_preferred_technicians_by_id(self, asset_id: int, user_id: int):
        params = {
            "assetID": asset_id,
            "userID": user_id
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_preferred_technicians_endpoint, params=params,
            headers=self.headers.basic_header(get_token())
            )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, f'{response.status_code}, {response.json()}'
        model = SuccessGetPreferredTechniciansModel(**response.json())
        logger.info(f'Successfully get preferred technicians with IDs: {user_id} for an asset with ID: {asset_id}.')
        return model

    @allure.step("Get preferred technicians from asset.")
    def get_preferred_technicians(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_preferred_technicians_endpoint,
            headers=self.headers.basic_header(get_token())
            )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, f'{response.status_code}, {response.json()}'
        model = SuccessGetPreferredTechniciansModel(**response.json())
        logger.info(f'Successfully get preferred technicians.')
        return model
