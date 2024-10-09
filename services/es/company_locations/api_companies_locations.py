import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.es.company_locations.payloads import Payloads
from services.es.company_locations.endpoints import Endpoints
from config.headers import Headers
from services.es.company_locations.models.company_locations_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
APP_ID = os.getenv('APP_ID')


class EsCompanyLocationsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Adds a location to the company.")
    def post_add_company_locations(self, company_id: int, location_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_company_locations_endpoint,
            headers=self.headers.auth_header(bearer_token=API_TOKEN, app_id=APP_ID),
            json=self.payloads.post_add_company_locations_payload(
                company_id=company_id,
                location_id=location_id
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, f'{response.json()}, {response.status_code}'
        logger.warning(f'Successfully adds a location to the company.')
