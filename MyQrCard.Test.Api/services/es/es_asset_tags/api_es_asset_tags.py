import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.es.es_asset_tags.payloads import Payloads
from services.es.es_asset_tags.endpoints import Endpoints
from config.headers import Headers
from services.es.es_asset_tags.models.es_asset_tags_model import *
import time
from http import HTTPStatus
from random import randint
from utils.token_utils import get_token


class EsAssetTagsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add tags to the asset.")
    def post_add_tags_to_asset(self, asset_id: int):
        name = f'Tag-{randint(1, 999)}'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_tags_to_asset_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_tags_to_asset_payload(asset_id, name)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, \
            (f'Expected status code {HTTPStatus.CREATED}, '
             f'but got {response.status_code}, {data_response}')
        model = SuccessAddTagsToAssetModel(result=response.json())
        logger.info(f'Successfully add tags to the asset with ID: {asset_id}.')
        return model

    @allure.step("Delete tags from asset.")
    def delete_tags_from_asset(self, asset_id: int, *name: str):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_tags_from_asset_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_tags_from_asset_payload(asset_id, *name)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            (f'Expected status code {HTTPStatus.ACCEPTED}, '
             f'but got {response.status_code}, {data_response}')
        logger.info(f'Successfully delete tags from asset with ID: {asset_id}.')
