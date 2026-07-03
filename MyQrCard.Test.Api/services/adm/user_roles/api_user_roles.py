import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.adm.user_roles.payloads import Payloads
from services.adm.user_roles.endpoints import Endpoints
from config.headers import Headers
from services.adm.user_roles.models.user_roles_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class AdmUserRolesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add roles to a user.")
    def post_add_roles_to_user(self, user_id: int, *roles_ids: int | tuple):
        start = time.time()
        response = requests.post(
            url=self.endpoints.add_roles_to_user_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.add_roles_to_user_payload(
                user_id,
                *roles_ids
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
        model = UserRolesResponseModel(root=response.json())
        logger.success(f'Successfully add a roles to user ID {user_id}.')
        return model

    @allure.step("Delete user's roles.")
    def delete_users_roles(self, user_id: int, *roles_ids: int | tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_users_roles_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_users_roles_payload(
                user_id,
                *roles_ids
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
        logger.success(f"Successfully delete user's roles.")
