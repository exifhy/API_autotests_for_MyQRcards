import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.es.es_asset_template_attributes.payloads import Payloads
from services.es.es_asset_template_attributes.endpoints import Endpoints
from config.headers import Headers
from services.es.es_asset_template_attributes.models.es_asset_template_attributes_model import *
import time
from http import HTTPStatus
from random import randint
from utils.token_utils import get_token


class EsAssetTemplateAttributesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Update attributes asset templates.")
    def post_update_attributes_asset_templates(self, asset_template_id: int, attribute_id: int):
        params = {
            "attributeID": attribute_id,
            "value": f"Строка {randint(1, 999)}",
            "isPublic": True,
            "sortOrder": 0
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_update_attributes_to_asset_template_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_update_attributes_to_asset_template_payload(
                asset_template_id,
                params
            )
        )
        end = time.time()
        data_response = self.response_content(response)
        self.attach_response(data_response)
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}.Message:{data_response}'
        logger.info(f'Successfully update attributes with ID: {attribute_id}, templates with ID: {asset_template_id}.')

    @allure.step("Delete attributes asset templates.")
    def post_delete_attributes_asset_templates(self, asset_template_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_update_attributes_to_asset_template_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_delete_attributes_from_asset_template_payload(asset_template_id)
        )
        end = time.time()
        data_response = self.response_content(response)
        self.attach_response(data_response)
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected {HTTPStatus.ACCEPTED}, but got {response.status_code}. Message:{data_response}'
        logger.info(f'Successfully update delete asset template with ID: {asset_template_id}.')
