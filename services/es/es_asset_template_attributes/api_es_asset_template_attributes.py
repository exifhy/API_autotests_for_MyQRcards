import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.es.es_asset_template_attributes.payloads import Payloads
from services.es.es_asset_template_attributes.endpoints import Endpoints
from config.headers import Headers
from services.es.es_asset_template_attributes.models.es_asset_template_attributes_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from random import randint


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


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
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_update_attributes_to_asset_template_payload(
                asset_template_id,
                params
            )
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Code:{response.status_code}.Message:{response.json()}'
        logger.info(f'Successfully update attributes with ID: {attribute_id}, templates with ID: {asset_template_id}.')
