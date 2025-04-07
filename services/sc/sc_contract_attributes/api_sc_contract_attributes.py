import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.sc.sc_contract_attributes.payloads import Payloads
from services.sc.sc_contract_attributes.endpoints import Endpoints
from config.headers import Headers
from services.sc.sc_contract_attributes.models.sc_contract_attributes_model import *
import time
from http import HTTPStatus
from random import randint
from utils.token_utils import get_token


class ScContractAttributesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Updates information about custom asset attributes.")
    def post_updates_info_about_custom_asset_attributes(self, contract_id: int, attribute_id: str) -> None:
        value = f"Attribute-{randint(1, 999)}"
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_updates_info_about_custom_object_attributes_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_updates_info_about_custom_object_attributes_payload(
                contract_id=contract_id,
                attribute_id=attribute_id,
                attribute_value=value
            )
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
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.info(f'Successfully updates information about custom asset attributes.')
        return None
