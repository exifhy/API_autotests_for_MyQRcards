import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.es.asset_districts.payloads import Payloads
from services.es.asset_districts.endpoints import Endpoints
from services.es.districts.api_districts import EsDistrictsAPI
from config.headers import Headers
import time
from http import HTTPStatus
from utils.token_utils import get_token


class EsAssetDistrictsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()
        self.districts = EsDistrictsAPI()

    @allure.step("Adds a districts to an object.")
    def add_district_to_object(self, asset_id: int, district_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.add_district_to_object_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.add_districts_payload(asset_id, district_id)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.CREATED, f'{response.status_code}, {response.json()}'
        logger.info(f'Successfully adds a districts to an object.')

    @allure.step("Adds a districts to an asset (args).")
    def add_districts_to_asset(self, asset_id: int, *district_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.add_district_to_object_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.add_new_districts_args_payload(asset_id, *district_id)
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
        assert response.status_code == HTTPStatus.CREATED, f'{response.status_code}, {response.json()}'
        logger.info(f'Successfully add a districts to an asset with ID: {district_id}.')

    @allure.step("Adds a districts to an object without default district.")
    def add_only_new_district_to_object(self, asset_id: int, district_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.add_district_to_object_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.add_new_districts_payload(asset_id, district_id)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully adds a new districts to an object.')

    @allure.step("Adds a default districts to an object.")
    def add_default_district_to_object(self, asset_id: int):
        default_district = None
        model_get_districts = self.districts.get_list_districts()
        for district in model_get_districts.result:
            if district.isDefault is True:
                default_district = district.id
        start = time.time()
        response = requests.post(
            url=self.endpoints.add_district_to_object_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.add_default_districts_payload(asset_id, default_district)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_request(response.request.body)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        logger.info(f'Successfully adds a default districts to an object.')

    @allure.step("Delete districts from the object.")
    def delete_district_from_object(self, asset_id: int, district_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_districts_from_object_endpoint,
            json=self.payloads.delete_districts_payload(asset_id, district_id),
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.ACCEPTED, f'{response.status_code}, {response.json()}'
        logger.info(f'Successfully delete the district from object, id object: {district_id}.')
