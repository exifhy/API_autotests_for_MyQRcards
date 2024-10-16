import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.common.common_attributes.payloads import Payloads
from services.common.common_attributes.endpoints import Endpoints
from config.headers import Headers
from services.common.common_attributes.models.common_attributes_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from random import randint

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
APP_ID = os.getenv('APP_ID')


class CommonAttributesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Attribute creation method for contract only.")
    def post_add_method_attributes_only_for_contract(self):
        attribute_name = f'Доп поле - {randint(1, 999)}'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_method_attributes_endpoint,
            headers=self.headers.auth_header(bearer_token=API_TOKEN, app_id=APP_ID),
            json=self.payloads.post_add_method_attributes_payloads(
                attribute_name=attribute_name,
                for_task=False,
                for_asset=False,
                for_check_list=False,
                fro_complete_work=False,
                for_contract=True,
                for_company=False
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
        assert response.status_code == HTTPStatus.CREATED, f'{response.status_code}, {response.json()}'
        model = SuccessAddAttributeModel(values=response.json())
        logger.warning(f'Successfully attribute creation method only for contract with name: {attribute_name}.')
        return model

    @allure.step("Attribute deletion method by ID.")
    def delete_method_attribute(self, attribute_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_method_attribute_endpoint(attribute_id),
            headers=self.headers.auth_header(bearer_token=API_TOKEN, app_id=APP_ID)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, f'{response.status_code}, {response.json()}'
        logger.warning(f'Successfully attribute deletion method by ID.')
