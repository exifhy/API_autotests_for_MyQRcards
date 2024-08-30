import random
import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.es.districts.payloads import Payloads
from services.es.districts.endpoints import Endpoints
from config.headers import Headers
from services.es.districts.models.districts_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from faker import Faker

fake_ru = Faker('ru_RU')

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class EsDistrictsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add district.")
    def post_add_district(self):
        district_name = fake_ru.street_title()
        notes_text = 'Участок создан авто-тестом'
        start = time.time()
        response = requests.post(
            url=self.endpoints.add_districts_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.add_districts_payload(
                district_name=district_name,
                notes=notes_text,
                status=False
            )
        )
        end = time.time()
        logger.info(response.headers)
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}'
        self.attach_response(response.json())
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        model = SuccessAddDistrictsModel(districts=response.json())
        logger.info(f'Successfully add a non-default district, name district: {district_name}')
        return model

    @allure.step("Marks the district as remote.")
    def delete_district_by_id(self, district_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.marks_districts_as_remote_by_id_endpoint(district_id),
            headers=self.headers.basic_header(API_TOKEN),
        )
        end = time.time()
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}'
        logger.info(response.headers)
        self.attach_time(start, end)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(f'Successfully marks the district with id: {district_id} as remote.')
