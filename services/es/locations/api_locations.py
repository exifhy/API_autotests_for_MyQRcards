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
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, f'{response.status_code}, {response.json()}'
        model = SuccessAddLocationModel(location=response.json())
        logger.info(f'Successfully add location. id: {model.location[0]}')
        return model.location[0]

    @allure.step("Delete location by ID.")
    def delete_location(self, location_id: int):
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
        logger.info(f'Successfully delete location by ID: {location_id}.')
