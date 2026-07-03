import random
import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.adm.adm_permissions_ui.payloads import Payloads
from services.adm.adm_permissions_ui.endpoints import Endpoints
from config.headers import Headers
from services.adm.adm_permissions_ui.models.adm_permissions_ui_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class AdmPermissionsUIAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get list permissions UI.")
    def get_list_permissions_ui(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_permissions_ui_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list of permissions ui.")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}, {data_response}')
        model = PermissionsUiGetResponseModel(root=response.json())
        logger.info(f'Successfully get list permissions UI.')
        return model

    @allure.step("Get permission UI by id.")
    def get_permission_ui_by_id(self, permission_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_permission_ui_by_id_endpoint(permission_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            (f'Expected status code {HTTPStatus.OK}, '
             f'but got {response.status_code}, {data_response}')
        model = PermissionsUiGetResultModel(**response.json())
        logger.info(f'Successfully get permissions UI by ID {permission_id}.')
        return model

    @allure.step("Delete permissions UI by id.")
    def delete_permissions_ui_by_id(self, permission_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_permission_ui_by_id(permission_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            (f'Expected status code {HTTPStatus.ACCEPTED}, '
             f'but got {response.status_code}, {data_response}')
        logger.warning(f'Successfully delete permissions UI by ID {permission_id}.')
        return None

    @allure.step("Delete permissions UI by list.")
    def delete_permissions_ui_by_list(self, *permission_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_permissions_ui_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_permissions_ui_by_list_payload(*permission_ids)
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
        logger.warning(f'Successfully delete permissions UI by list {permission_ids}.')
        return None

    @allure.step("Add permission UI.")
    def post_add_permission_ui(self):
        data = {
            "code": f"task@A{random.randint(1000000, 9999999)}",
            "description": "Авто тест",
            "mustBeAssignedToRole": False,
            "allowReadonlyOnly": False
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_permissions_ui_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_permissions_ui_payload(data)
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
        model = PermissionsUiAddResponseModel(results=response.json())
        logger.info(f'Successfully add permission UI.')
        return model

    @allure.step("Add three permissions UI.")
    def post_add_three_permissions_ui(self):
        data = {
            "code": f"task@A{random.randint(1000000, 9999999)}",
            "description": "Авто тест1",
            "mustBeAssignedToRole": False,
            "allowReadonlyOnly": False
        }
        data2 = {
            "code": f"task@A{random.randint(1000000, 9999999)}",
            "description": "Авто тест2",
            "mustBeAssignedToRole": False,
            "allowReadonlyOnly": False
        }
        data3 = {
            "code": f"task@A{random.randint(1000000, 9999999)}",
            "description": "Авто тест3",
            "mustBeAssignedToRole": False,
            "allowReadonlyOnly": False
        }

        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_permissions_ui_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_permissions_ui_payload(data, data2, data3)
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
        model = PermissionsUiAddResponseModel(results=response.json())
        logger.info(f'Successfully add permission UI.')
        return model

    @allure.step("Update permission UI.")
    def put_update_permission_ui(self, permission_id: int):
        model_before = self.get_permission_ui_by_id(permission_id)
        data = {
            "code": f"task@U{random.randint(1000000, 9999999)}",
            "description": "Изменено авто тестом",
            "mustBeAssignedToRole": True,
            "allowReadonlyOnly": True,
            "id": permission_id
        }
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_permissions_ui_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_permissions_ui_payload(data)
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
        model_after = self.get_permission_ui_by_id(permission_id)
        assert model_before.code != model_after.code, \
            f"{model_before.code} is equal {model_after.code}, permission not updated."
        assert model_before.description != model_after.description, \
            f"{model_before.description} is equal {model_after.description}, permission not updated."
        assert model_before.mustBeAssignedToRole != model_after.mustBeAssignedToRole, \
            f"{model_before.mustBeAssignedToRole} is equal {model_after.mustBeAssignedToRole}, permission not updated."
        assert model_before.allowReadonlyOnly != model_after.allowReadonlyOnly, \
            f"{model_before.allowReadonlyOnly} is equal {model_after.allowReadonlyOnly}, permission not updated."
        logger.info(f'Successfully update permission UI with ID {permission_id}.')
        return None
