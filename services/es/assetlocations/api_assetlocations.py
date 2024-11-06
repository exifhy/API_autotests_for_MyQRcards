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

    @allure.step("Adds a location to an asset.")
    def add_location_to_object(self, asset_id: int, location_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.add_location_to_object_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.add_location_to_object_payload(asset_id, location_id)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, f'{response.status_code},{response.json()}'
        logger.info(f'Successfully add a location to an object.')

    @allure.step("Deleting location binding to an asset.")
    def delete_location_from_object(self, asset_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_of_location_from_object_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.unbind_of_location_from_object_payload(asset_id)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, f'{response.status_code}, {response.json()}'
        logger.info(f'Successfully unbind of location from object.')

    @allure.step("Get list of locations by asset.")
    def get_location_by_object(self, asset_id: int):
        params = {
            "assetID": asset_id
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_location_by_object_endpoint, params=params,
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            f'{response.status_code}, {response.json()}'
        model = SuccessGetAssetLocationModel(root=response.json())
        logger.info(f'Successfully get list of locations by asset.')
        return model

    @allure.step("Updating the time an asset is on location.")
    def put_update_time_an_asset_on_location(self, asset_id: int, location_id: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_time_an_asset_on_location_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.add_location_to_object_payload(
                asset_id=asset_id,
                location_id=location_id
            )
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'{response.status_code}, {response.json()}'
        logger.info(f'Successfully updating the time an asset is on location.')
