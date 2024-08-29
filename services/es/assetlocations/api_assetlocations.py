import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.es.assetlocations.payloads import Payloads
from services.es.assetlocations.endpoints import Endpoints
from config.headers import Headers
from services.es.assetlocations.models.assetlocations_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class EsAssetLocationsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Adds a location to an object.")
    def add_location_to_object(self, asset_id: int, location_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.add_location_to_object_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.add_location_to_object_payload(asset_id, location_id)
        )
        end = time.time()
        logger.info(response.headers)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}'
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        logger.info(f'Successfully add a location to an object.')

    @allure.step("Deleting location binding to an object.")
    def unbind_of_location_from_object(self, asset_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.unbind_of_location_from_object_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.unbind_of_location_from_object_payload(asset_id)
        )
        end = time.time()
        logger.info(response.headers)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}'
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        logger.info(f'Successfully unbind of location from object.')
