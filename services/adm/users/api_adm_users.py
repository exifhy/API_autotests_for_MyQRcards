from urllib import parse
import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from src.generators.generators import generated_user
from services.adm.users.payloads import Payloads
from services.adm.users.endpoints import Endpoints
from config.headers import Headers
from services.adm.users.models.adm_users_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class AdmUsersAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()
        self.user = next(generated_user())

    @allure.step("Add user customer.")
    def post_add_user_customer(self):
        params = {
            "skipAccountVerification": True
        }
        user_name = self.user.name
        user_surname = self.user.surname
        user_email = self.user.email
        user_phone = self.user.phone
        start = time.time()
        response = requests.post(
            url=self.endpoints.add_users_endpoint, params=params,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.add_user_customer_payload(
                name=user_name,
                surname=user_surname,
                email=user_email,
                phone=user_phone
            )
        )
        end = time.time()
        logger.info(response.headers)
        logger.warning(response.request.url)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}'
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        model = SuccessUserModel(**response.json())
        logger.info(f'Successfully add a user customer name: {user_name}')
        return model

    @allure.step("Add user employee.")
    def post_add_user_staff(self):
        params = {
            "skipAccountVerification": True
        }
        user_name = self.user.name
        user_surname = self.user.surname
        user_email = self.user.email
        user_phone = self.user.phone
        start = time.time()
        response = requests.post(
            url=self.endpoints.add_users_endpoint, params=params,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.add_user_staff_payload(
                name=user_name,
                surname=user_surname,
                email=user_email,
                phone=user_phone
            )
        )
        end = time.time()
        logger.info(response.headers)
        logger.warning(response.request.url)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}'
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        model = SuccessUserModel(**response.json())
        logger.info(f'Successfully add a user staff name {user_name}')
        return model

    @allure.step("Marks the user as remote.")
    def delete_user_by_id(self, user_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_user_by_id_endpoint(user_id),
            headers=self.headers.basic_header(API_TOKEN),
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}'
        self.attach_time(start, end)
        logger.info(f'Successfully marks the user with id: {user_id} as remote.')

    @allure.step('Get detail user info.')
    def get_user_info_by_id(self, user_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_user_info_by_id_endpoint(user_id),
            headers=self.headers.basic_header(API_TOKEN),
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.OK, f'Status code {response.status_code}'
        self.attach_time(start, end)
        model = SuccessGetDetailedInfoUserModel(**response.json())
        logger.info(f'Successfully received detail user info.')
        return model
