import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.es.es_asset_attributes.payloads import Payloads
from services.es.es_asset_attributes.endpoints import Endpoints
from config.headers import Headers
from services.es.es_asset_attributes.models.es_asset_attributes_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token
from random import randint


class EsAssetAttributesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Update assets attributes.")
    def post_update_attributes_assets(self, asset_id: int, attribute_id: int):
        value = f"Значение поля {randint(99, 999)}"
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_update_attributes_assets_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_update_attributes_assets_payload(
                asset_id,
                attribute_id,
                value=value
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully update assets attributes.')
