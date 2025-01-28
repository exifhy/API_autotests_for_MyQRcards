import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.es.es_asset_template_districts.payloads import Payloads
from services.es.es_asset_template_districts.endpoints import Endpoints
from config.headers import Headers
from services.es.es_asset_template_districts.models.es_asset_template_districts_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class EsAssetTemplateDistrictsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add districts to asset templates.")
    def post_districts_to_asset_templates(self, asset_template_id: int, *districts_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_districts_to_asset_templates_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_districts_to_asset_templates_payload(asset_template_id, *districts_id)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response_headers(response.headers)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected {HTTPStatus.CREATED}, but got {response.status_code}. Message:{data_response}'
        model = SuccessAddDistrictsToAssetTemplatesModel(result=response.json())
        logger.info(f'Successfully add districts with ID: {districts_id} to templates with ID: {asset_template_id}.')
        return model

    @allure.step("Delete districts from asset templates.")
    def delete_districts_from_asset_templates(self, asset_template_id: int, *districts_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_districts_from_asset_templates_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_districts_from_asset_templates_payload(asset_template_id, *districts_id)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response_headers(response.headers)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected {HTTPStatus.ACCEPTED}, but got {response.status_code}. Message:{data_response}'
        logger.warning(f'Successfully delete districts with ID: {districts_id} from templates ID: {asset_template_id}.')

    @allure.step("Delete districts from asset template by ID.")
    def delete_districts_from_asset_template_by_id(self, asset_template_id: int, *districts_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_districts_from_asset_template_by_id_endpoint(asset_template_id),
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_districts_from_asset_template_by_id_payload(*districts_id)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response_headers(response.headers)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected {HTTPStatus.ACCEPTED}, but got {response.status_code}. Message:{data_response}'
        logger.warning(f'Successfully delete districts with ID: {districts_id} from template by ID: {asset_template_id}.')
