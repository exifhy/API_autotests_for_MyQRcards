from requests import JSONDecodeError
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
from dotenv import load_dotenv
import os
from random import randint

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class ScContractAttributesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Updates information about custom object attributes.")
    def post_updates_info_about_custom_object_attributes(self, contract_id: int, attribute_id: str):
        value = f"Attribute-{randint(1, 999)}"
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_updates_info_about_custom_object_attributes_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_updates_info_about_custom_object_attributes_payload(
                contract_id=contract_id,
                attribute_id=attribute_id,
                attribute_value=value
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
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully updates information about custom object attributes.')
