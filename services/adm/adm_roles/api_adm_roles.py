import random
import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.adm.adm_roles.payloads import Payloads
from services.adm.adm_roles.endpoints import Endpoints
from config.headers import Headers
from services.adm.adm_roles.models.adm_roles_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class AdmRolesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get list roles for tenant.")
    def get_list_roles(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_roles_endpoint,
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
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list of roles.")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}, {data_response}')
        model = SuccessGetListRolesModel(results=response.json())
        logger.info(f'Successfully get list roles for tenant.')
        return model

    @allure.step("Get list applications role by role ID.")
    def get_list_applications_role_by_role_id(self, role_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_roles_applications_endpoint(role_id),
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
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list of  applications roles.")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}, {data_response}')
        model = RoleApplicationsResponseModel(root=response.json())
        logger.info(f'Successfully get list applications role by role ID {role_id}.')
        return model

    @allure.step("Get list attachments role by role ID.")
    def get_list_attachments_role_by_role_id(self, role_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_roles_attachments_endpoint(role_id),
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
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list of  attachments roles.")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}, {data_response}')
        model = RoleAttachmentsListResponseModel(results=response.json())
        logger.info(f'Successfully get list attachments role by role ID {role_id}.')
        return model

    @allure.step("Get role by ID.")
    def get_role_by_id(self, role_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_role_by_id_endpoint(role_id),
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
        model = RoleGetResultResponseModel(**response.json())
        logger.info(f'Successfully get role by ID {role_id}.')
        return model

    @allure.step("Delete role by ID.")
    def delete_role_by_id(self, role_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_role_by_id_endpoint(role_id),
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
        logger.warning(f'Successfully delete role by ID {role_id}.')
        return None

    @allure.step("Add role.")
    def post_add_role(self):
        data = {
            "name": f"Роль-{random.randint(1, 9999)}",
            "description": "Роль создана авто тестом."
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_roles_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_roles_payload(data)
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
        model = SuccessAddRoleResponseModel(results=response.json())
        logger.info(f'Successfully add role.')
        return model

    @allure.step("Add three roles.")
    def post_add_three_roles(self):
        data = {
            "name": f"Роль-{random.randint(1, 9999)}",
            "description": "Роль создана авто тестом 1."
        }
        data2 = {
            "name": f"Роль-{random.randint(1, 9999)}",
            "description": "Роль создана авто тестом 2."
        }
        data3 = {
            "name": f"Роль-{random.randint(1, 9999)}",
            "description": "Роль создана авто тестом 3."
        }

        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_roles_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_roles_payload(data, data2, data3)
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
        model = SuccessAddRoleResponseModel(results=response.json())
        logger.info(f'Successfully add three roles {model}.')
        return model

    @allure.step("Update role.")
    def put_update_role(self, role_id: int):
        model_before = self.get_role_by_id(role_id)
        data = {
            "id": role_id,
            "name": f"Обновленная роль-{random.randint(1, 9999)}",
            "description": "Роль обновлена авто тестом."
        }
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_role_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_roles_payload(data)
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
        model_after = self.get_role_by_id(role_id)
        assert model_before.name != model_after.name, \
            f"{model_before.name} is equal {model_after.name}"
        assert model_before.description != model_after.description, \
            f"{model_before.description} is equal {model_after.description}"
        logger.info(f'Successfully update role by ID {role_id}.')
        return None

    @allure.step("Delete roles by list.")
    def delete_roles_by_list(self, *role_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_roles_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_roles_by_list_payload(*role_ids)
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
        logger.warning(f'Successfully delete role by list {role_ids}.')
        return None

    @allure.step("Copy role.")
    def post_copy_roles(self, role_id: int):
        data = {
            "copiedRoleID": role_id,
            "name": f"Копия роли-{role_id}",
            "description": "Копия сделана авто тестом."
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_roles_copy_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_copy_roles_payload(data)
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
        model = SuccessAddCopyRolesResponseModel(results=response.json())
        logger.info(f'Successfully copy role by ID {role_id}.')
        return model

    @allure.step("Get list role permissions api.")
    def get_role_permissions_api(self, role_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_roles_permissions_api_endpoint(role_id),
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
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list of roles permissions API.")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}, {data_response}')
        model = RolePermissionsApiListResponseModel(root=response.json())
        logger.info(f'Successfully get role permissions api {role_id}.')
        return model

    @allure.step("Get list role permissions ext.")
    def get_role_permissions_ext(self, role_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_roles_permissions_ext_endpoint(role_id),
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
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list of roles permissions ext.")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}, {data_response}')
        model = RolePermissionsExtListResponseModel(root=response.json())
        logger.info(f'Successfully get role permissions ext {role_id}.')
        return model

    @allure.step("Get list role permissions UI.")
    def get_role_permissions_ui(self, role_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_roles_permissions_ui_endpoint(role_id),
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
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list of roles permissions UI.")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}, {data_response}')
        model = RolePermissionsUiListResponseModel(root=response.json())
        logger.info(f'Successfully get role permissions UI {role_id}.')
        return model
