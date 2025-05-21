import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.adm.adm_role_permissions_ext.payloads import Payloads
from services.adm.adm_role_permissions_ext.endpoints import Endpoints
from config.headers import Headers
from services.adm.adm_role_permissions_ext.models.adm_role_permissions_ext_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class AdmRolePermissionsExtAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add role permissions Ext.")
    def post_role_permissions_ext(self, role_id: int, *permissions_ids: int or tuple):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_role_permissions_ext_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_role_permissions_ext_payload(
                role_id,
                *permissions_ids
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
        model = RolePermissionsExtListResponseModel(results=response.json())
        logger.info(f'Successfully add role permissions Ext.')
        return model

    @allure.step("Delete role permissions Ext.")
    def delete_role_permissions_ext(self, role_id: int, *permissions_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_role_permissions_ext_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_role_permissions_ext_payload(
                role_id,
                *permissions_ids
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
        logger.warning(f'Successfully delete role ID {role_id} permissions Ext ID {permissions_ids}.')
        return None
