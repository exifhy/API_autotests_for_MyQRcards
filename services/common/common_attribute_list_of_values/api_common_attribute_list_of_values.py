import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.common.common_attribute_list_of_values.payloads import Payloads
from services.common.common_attribute_list_of_values.endpoints import Endpoints
from config.headers import Headers
from services.common.common_attribute_list_of_values.models.common_attribute_list_of_values_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from random import randint
from faker import Faker


faker_ru = Faker('ru_RU')


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
APP_ID = os.getenv('APP_ID')


class CommonAttributeListOfValuesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add attribute the list of available values with five fields.")
    def post_add_attribute_list_of_value_with_five_fields(self, attribute_id: int) -> dict:
        """Function returns dictionary with all values."""
        values = [
            {"key": f'ключ: {randint(1, 99)}', "value": faker_ru.color_name()},
            {"key": f'ключ: {randint(100, 199)}', "value": faker_ru.color_name()},
            {"key": f'ключ: {randint(200, 299)}', "value": faker_ru.color_name()},
            {"key": f'ключ: {randint(300, 499)}', "value": faker_ru.color_name()},
            {"key": f'ключ: {randint(500, 599)}', "value": faker_ru.color_name()}
        ]
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_attribute_list_of_value_endpoint,
            headers=self.headers.auth_header(bearer_token=API_TOKEN, app_id=APP_ID),
            json=self.payloads.post_add_attribute_list_of_value_payload(
                attribute_id,
                *values
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
        assert response.status_code == HTTPStatus.ACCEPTED, f'{response.status_code}, {response.json()}'
        logger.warning(f'Successfully add attribute the list of available values.')
        result = {item['key']: item['value'] for item in values}
        return result

