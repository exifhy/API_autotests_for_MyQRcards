import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.adm.user_districts.payloads import Payloads
from services.adm.user_districts.endpoints import Endpoints
from config.headers import Headers
from services.adm.user_districts.models.user_districts_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


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
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.add_districts_to_user_payload(
                districts_id,
                user_id,
                schedule_id=None
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
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        logger.info(f'Successfully add of a district to a user, district id: {districts_id}, user id: {user_id}.')
        return None

    @allure.step("Add three districts to user.")
    def post_add_three_districts_to_user(self, user_id: int, model_districts):
        data = {
            "districtID": model_districts.districts[0]
        }
        data2 = {
            "districtID": model_districts.districts[1]
        }
        data3 = {
            "districtID": model_districts.districts[2]
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.add_districts_to_user_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_districts_to_user_payload(
                user_id, data, data2, data3
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
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        logger.info(f'Successfully add of a district to a user, district id: {model_districts}, user id: {user_id}.')
        return None

    @allure.step("Delete districts from user.")
    def delete_districts_from_user(self, user_id: int, *districts_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_districts_from_user_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_districts_from_user_payload(
                user_id,
                *districts_ids
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
        logger.info(f'Successfully delete districts from user, district ID: {districts_ids}, user id: {user_id}.')
        return None

    @allure.step("Update districts user.")
    def put_update_districts_user(self, user_id: int, model_districts):
        data = {
            "districtID": model_districts.districts[0],
            "scheduleRuleID": None
        }
        data2 = {
            "districtID": model_districts.districts[1],
            "scheduleRuleID": None
        }
        data3 = {
            "districtID": model_districts.districts[2],
            "scheduleRuleID": None
        }
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_user_districts_update_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_districts_user_payload(
                user_id,
                data, data2, data3
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
        logger.info(f'Successfully update districts user, districts id: {model_districts}, user id: {user_id}.')
        return None
