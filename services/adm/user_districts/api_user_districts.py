import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.adm.user_districts.payloads import Payloads
from services.adm.user_districts.endpoints import Endpoints
from config.headers import Headers
from services.adm.user_districts.models.user_districts_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class AdmUserDistrictsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add districts to user.")
    def post_add_districts_to_user(self, districts_id: int, user_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.add_districts_to_user_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.add_districts_to_user_payload(
                districts_id,
                user_id,
                schedule_id=None
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
        assert response.status_code == HTTPStatus.CREATED, f'{response.status_code}, {response.json()}'
        logger.info(f'Successfully add of a district to a user, district id: {districts_id}, user id: {user_id}.')

