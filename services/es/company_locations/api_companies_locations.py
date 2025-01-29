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
        data_response = self.response_content(response)
        logger.info(response.headers)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.info(f'Successfully adds a location to the company.')

    @allure.step("Get list locations from company.")
    def get_list_locations_company(self, company_id: int):
        params = {
            "companyID": company_id
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_company_locations_endpoint, params=params,
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            f'Expected {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        model = SuccessGetListCompanyLocationsModel(root=response.json())
        logger.info(f'Successfully get location from company with ID {company_id}.')
        return model

    @allure.step("Get list locations from company with asserts.")
    def get_list_locations_company_with_asserts(self, company_id: int, location_id: int, deleted: bool):
        params = {
            "companyID": company_id
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_company_locations_endpoint, params=params,
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if deleted is True:
            assert response.status_code == HTTPStatus.NO_CONTENT, \
                f'Expected {HTTPStatus.NO_CONTENT}, but got {response.status_code}'
            logger.info(f'Successfully get deleted location from company with ID {company_id}.')
        if deleted is False:
            assert response.status_code == HTTPStatus.OK, \
                f'Expected {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
            model = SuccessGetListCompanyLocationsModel(root=response.json())
            assert location_id == model.root[str(location_id)].location.id, \
                f'Location with ID {location_id} not in list company locations'
            logger.info(f'Successfully get list locations from company with ID {company_id}.')
            return model

    @allure.step("Get list deleted locations from company.")
    def get_list_deleted_locations_company(self, company_id: int):
        params = {
            "companyID": company_id
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_company_locations_endpoint, params=params,
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.NO_CONTENT, \
            f'Expected {HTTPStatus.NO_CONTENT}, but got {response.status_code}. Message {data_response}'
        logger.info(f'Successfully get list deleted locations from company.')

    @allure.step("Update location from company.")
    def put_update_location_from_company(self, company_id: int, location_id: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_company_location_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.put_update_location_from_company_payload(
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
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, f'{response.json()}, {response.status_code}'
        logger.info(f'Successfully update location from company.')

    @allure.step("Delete location from company.")
    def delete_location_from_company(self, company_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_locations_from_company_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_location_from_company_payload(
                company_id=company_id
            )
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected {HTTPStatus.ACCEPTED}, but got {response.status_code}. Message {data_response}'
        logger.warning(f'Successfully delete location from company with ID {company_id}.')
