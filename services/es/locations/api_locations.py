from requests import JSONDecodeError
import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.es.locations.payloads import Payloads
from services.es.locations.endpoints import Endpoints
from config.headers import Headers
from services.es.locations.models.locations_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from random import randint

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class EsLocationsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add a location.")
    def post_add_location(self):
        start = time.time()
        response = requests.post(
            url=self.endpoints.add_locations_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.add_location_payload(
                address=f"Невский проспект, {randint(1, 300)}, Санкт-Петербург, Россия",
                coordinate="59.932741:30.349137",
                timezoneUtcOffsetMinutes=180,
                countryTwoSymbolCode="RU"
            )
        )
        end = time.time()
        data_response = self.response_content(response)
        self.attach_response(data_response)
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessAddLocationModel(location=response.json())
        logger.info(f'Successfully add location. id: {model.location[0]}')
        return model.location[0]

    @allure.step("Delete location by ID.")
    def delete_location_by_id(self, location_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_location_by_id(location_id),
            headers=self.headers.basic_header(API_TOKEN),
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code in {HTTPStatus.ACCEPTED, HTTPStatus.PARTIAL_CONTENT}, (f'{response.status_code}, '
                                                                                           f'{response.json()}')
        logger.warning(f'Successfully delete location by ID: {location_id}.')

    @allure.step("Delete the locations by list.")
    def delete_locations_by_list(self, *args):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_locations_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_locations_payload(*args)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Status code {response.status_code}, {response.json()}'
        logger.warning(f'Successfully delete the locations by list with ID: {args}.')

    @allure.step("Get list locations.")
    def get_list_locations(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_locations_endpoint,
            headers=self.headers.basic_header(API_TOKEN)
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
        assert response.status_code == HTTPStatus.OK, \
            f'Status code {response.status_code}, {response.json()}'
        model = SuccessGetListLocationsModel(root=response.json())
        logger.info(f'Successfully get list locations.')
        return model

    @allure.step("Update location.")
    def put_update_location(self, location_id: int):
        params = {
            "id": location_id,
            "address": f"Невский проспект, {randint(301, 900)}, Санкт-Петербург, Россия",
            "coordinate": "59.978309668788185:30.31483684679914",
            "description": "Локация изменена авто тестом.",
            "timezoneUtcOffsetMinutes": 180,
            "countryTwoSymbolCode": "RU"
        }
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_location_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.put_update_location_payload(params)
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
        logger.info(f'Successfully update location with Id: {location_id}')

    @allure.step("Get head locations.")
    def head_locations(self):
        start = time.time()
        response = requests.head(
            url=self.endpoints.head_return_quantity_locations,
            headers=self.headers.basic_header(API_TOKEN)
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
        assert response.status_code == HTTPStatus.OK, \
            f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully get head locations.')

    @allure.step("Delete (remove) location by ID.")
    def delete_location_by_id_remove(self, location_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.remove_location_by_id_endpoint(location_id),
            headers=self.headers.basic_header(API_TOKEN)
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
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Status code {response.status_code}, {response.json()}'
        logger.warning(f'Successfully remove location by id with ID: {location_id}.')

    @allure.step("Delete (remove) location by list.")
    def delete_location_by_list_remove(self, *location_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.remove_locations_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_locations_by_list_remove_payload(*location_ids)
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
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Status code {response.status_code}, {response.json()}'
        logger.warning(f'Successfully remove location by list with IDs: {location_ids}.')

    @allure.step("Get location by ID.")
    def get_location_by_id(self, location_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_location_by_id_endpoint(location_id),
            headers=self.headers.basic_header(API_TOKEN),
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
        assert response.status_code == HTTPStatus.OK, \
            f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully get location with ID: {location_id}.')
