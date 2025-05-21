import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.adm.adm_role_applications.payloads import Payloads
from services.adm.adm_role_applications.endpoints import Endpoints
from config.headers import Headers
from services.adm.adm_role_applications.models.adm_role_applications_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class AdmRoleApplicationsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add role applications.")
    def post_role_applications(self, role_id: int, *app_ids: int or tuple):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_role_applications_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_role_applications_payload(
                role_id,
                *app_ids
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
            (f'Expected status code {HTTPStatus.CREATED}, '
             f'but got {response.status_code}, {data_response}')
        model = RoleApplicationsListResponseModel(results=response.json())
        logger.info(f'Successfully add role applications.')
        return model

    @allure.step("Delete role applications.")
    def delete_role_applications(self, role_id: int, *app_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_role_applications_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_role_applications_payload(
                role_id,
                *app_ids
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
            (f'Expected status code {HTTPStatus.ACCEPTED}, '
             f'but got {response.status_code}, {data_response}')
        logger.warning(f'Successfully delete role ID {role_id} applications ID {app_ids}.')
        return None
