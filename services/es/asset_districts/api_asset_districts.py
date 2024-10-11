import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.es.asset_districts.payloads import Payloads
from services.es.asset_districts.endpoints import Endpoints
from config.headers import Headers
from services.es.asset_districts.models.asset_districts_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class EsAssetDistrictsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Adds a districts to an object.")
    def add_district_to_object(self, asset_id: int, district_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.add_district_to_object_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
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
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}'
        logger.info(f'Successfully adds a districts to an object.')

    @allure.step("Adds a districts to an object without default district.")
    def add_only_new_district_to_object(self, asset_id: int, district_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.add_district_to_object_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
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
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code, response.json()}'
        logger.info(f'Successfully adds a new districts to an object.')

    @allure.step("Adds a default districts to an object.")
    def add_default_district_to_object(self, asset_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.add_district_to_object_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.add_default_districts_payload(asset_id)
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
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}'
        logger.info(f'Successfully adds a default districts to an object.')

    @allure.step("Delete districts from the object.")
    def delete_district_from_object(self, asset_id: int, district_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_districts_from_object_endpoint,
            json=self.payloads.delete_districts_payload(asset_id, district_id),
            headers=self.headers.basic_header(API_TOKEN),
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_time(start, end)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}'
        logger.info(f'Successfully delete the district from object, id object: {district_id}.')
