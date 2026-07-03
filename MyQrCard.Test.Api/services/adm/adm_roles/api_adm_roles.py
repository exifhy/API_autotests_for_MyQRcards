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
from utils.env import get_app_id
import concurrent.futures


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
        logger.success(f'Successfully get list roles for tenant.')
        return model

    @allure.step("Get list roles for tenant, return role id by name.")
    def get_list_roles_return_role_id_by_name(self, name_role: str):
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
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessGetListRolesModel(results=response.json())
        role_id = None
        for role in model.results:
            if role.name == name_role:
                role_id = role.id
                break
        logger.success(f'Successfully get list roles for tenant and return role id by role name.')
        return role_id

    @allure.step("Get list roles isDeleted=false.")
    def get_list_roles_undeleted(self):
        params = {
            "isDeleted": False
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_roles_endpoint, params=params,
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
        logger.success(f'Successfully get list roles isDeleted=false.')
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
        logger.success(f'Successfully get list applications role by role ID {role_id}.')
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
        logger.success(f'Successfully get list attachments role by role ID {role_id}.')
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
        logger.success(f'Successfully get role by ID {role_id}.')
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
        logger.success(f'Successfully delete role by ID {role_id}.')
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
        logger.success(f'Successfully add role.')
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
        logger.success(f'Successfully add three roles {model}.')
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
        logger.success(f'Successfully update role by ID {role_id}.')
        return None

    @allure.step("Delete roles by list.")
    def delete_roles_by_list(self, *role_ids: int | tuple):
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
        logger.success(f'Successfully delete role by list {role_ids}.')
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
        logger.success(f'Successfully copy role by ID {role_id}.')
        return model
    
    @allure.step("Get list roles packages by role ID.")
    def get_list_roles_packages_by_id(self, role_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_roles_packages_by_id_endpoint(role_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code  in {HTTPStatus.OK, HTTPStatus.NO_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.NO_CONTENT}, '
             f'but got {response.status_code}, {data_response}')
        if response.status_code == HTTPStatus.OK:
            model = SuccessRolePackagesListResultModel(root=response.json())
            logger.success(f'Successfully get list roles packages by role ID.')
            return model
        elif response.status_code == HTTPStatus.NO_CONTENT:
            logger.success(f'Successfully get list roles packages by role ID. NO CONTENT.')
            return None
        
    @allure.step("Get list roles packages by role ID, return ID role package.")
    def get_list_roles_packages_by_id_return_role_package(self, role_id: int, package_id: str):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_roles_packages_by_id_endpoint(role_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code  == HTTPStatus.OK, \
            (f'Expected status code {HTTPStatus.OK}, '
             f'but got {response.status_code}, {data_response}')
        model = SuccessRolePackagesListResultModel(root=response.json())
        logger.success(f'Successfully get list roles packages by role ID.')
        for key, item in model.root.items():
            if item.packageID == package_id:
                logger.success(f'Successfully get role package with ID {key}.')
                return key

    @allure.step("Get list roles packages without token.")
    def get_list_roles_packages_without_token(self, role_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_roles_packages_by_id_endpoint(role_id),
            headers=self.headers.without_authorization_field_header(get_app_id())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, \
            (f'Expected status code {HTTPStatus.UNAUTHORIZED}, '
             f'but got {response.status_code}, {data_response}')
        logger.success(f'Successfully verified unauthorized access.')
        return response

    @allure.step("Get list roles packages with invalid token.")
    def get_list_roles_packages_invalid_token(self, role_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_roles_packages_by_id_endpoint(role_id),
            headers=self.headers.basic_header('invalid_token')
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, \
            (f'Expected status code {HTTPStatus.UNAUTHORIZED}, '
             f'but got {response.status_code}, {data_response}')
        logger.success(f'Successfully verified invalid token handling.')
        return response

    @allure.step("Get list roles packages with invalid app id.")
    def get_list_roles_packages_invalid_app_id(self, role_id: int):
        start = time.time()
        expected_message = "Не найден обязательный заголовок [X-Application-ID]."
        response = requests.get(
            url=self.endpoints.get_list_roles_packages_by_id_endpoint(role_id),
            headers=self.headers.auth_header(get_token(), "invalid app id")
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            (f'Expected status code {HTTPStatus.FORBIDDEN}, '
             f'but got {response.status_code}, {data_response}')
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].message == expected_message, \
            f"Expected {expected_message}, but got {model.list_model[0].message}"
        logger.success(f'Successfully verified invalid app id handling.')
        return model

    @allure.step("Get list roles packages with content type {content_type}.")
    def get_list_roles_packages_with_content_type(self, role_id: int, content_type: str):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_roles_packages_by_id_endpoint(role_id),
            headers=self.headers.basic_header_content_type(get_token(), content_type)
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
        model = SuccessRolePackagesListResultModel(root=response.json())
        logger.success(f'Successfully get list roles packages with content type {content_type}.')
        return model

    @allure.step("Get list roles packages measure response time.")
    def get_list_roles_packages_measure_time(self, role_id: int, threshold_ms: int = 200):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_roles_packages_by_id_endpoint(role_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        response_time_ms = (end - start) * 1000
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response_time_ms < threshold_ms, \
            (f'Response time {response_time_ms:.2f}ms exceeds threshold {threshold_ms}ms')
        assert response.status_code == HTTPStatus.OK, \
            (f'Expected status code {HTTPStatus.OK}, '
             f'but got {response.status_code}, {data_response}')
        model = SuccessRolePackagesListResultModel(root=response.json())
        logger.success(f'Successfully measured response time: {response_time_ms:.2f}ms')
        return model, response_time_ms

    @allure.step("Get list roles packages idempotency.")
    def get_list_roles_packages_idempotent(self, role_id: int):
        start = time.time()
        response1 = requests.get(
            url=self.endpoints.get_list_roles_packages_by_id_endpoint(role_id),
            headers=self.headers.basic_header(get_token())
        )
        response2 = requests.get(
            url=self.endpoints.get_list_roles_packages_by_id_endpoint(role_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response1.headers)
        logger.info(response2.headers)
        self.attach_response_headers(response1.headers)
        self.attach_response_headers(response2.headers)
        data_response1 = self.response_content(response1)
        data_response2 = self.response_content(response2)
        self.attach_response(data_response1)
        self.attach_response(data_response2)
        self.attach_time(start, end)
        self.attach_url(response1.request.url)
        assert response1.status_code == response2.status_code, \
            (f'Status codes differ: {response1.status_code} vs {response2.status_code}')
        if response1.status_code == HTTPStatus.OK and response2.status_code == HTTPStatus.OK:
            assert response1.json() == response2.json(), "Responses differ between requests"
        assert response1.status_code == HTTPStatus.OK, \
            (f'Expected status code {HTTPStatus.OK}, '
             f'but got {response1.status_code}, {data_response1}')
        model = SuccessRolePackagesListResultModel(root=response1.json())
        logger.success(f'Successfully verified idempotency.')
        return model

    @allure.step("Get list roles packages concurrent requests.")
    def get_list_roles_packages_concurrent(self, role_id: int, num_requests: int = 10):
        def make_request():
            return requests.get(
                url=self.endpoints.get_list_roles_packages_by_id_endpoint(role_id),
                headers=self.headers.basic_header(get_token())
            )
        start = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
            futures = [executor.submit(make_request) for _ in range(num_requests)]
            responses = [future.result() for future in futures]
        end = time.time()
        success_count = sum(1 for r in responses if r.status_code == HTTPStatus.OK)
        self.attach_time(start, end)
        assert success_count == num_requests, \
            (f'Not all requests succeeded. Status codes: {[r.status_code for r in responses]}')
        logger.success(f'Successfully completed {num_requests} concurrent requests. OK: {success_count}')
        return responses

    @allure.step("Get list roles packages verify forbidden access.")
    def get_list_roles_packages_forbidden(self, role_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_roles_packages_by_id_endpoint(role_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code != HTTPStatus.FORBIDDEN, \
            (f'Got unexpected forbidden status code {HTTPStatus.FORBIDDEN}, '
             f'but should have access, {data_response}')
        logger.success(f'Successfully verified access is not forbidden.')
        return response

    @allure.step("Add packages to role.")
    def post_add_roles_packages(self, role_id: int, package_id: str, package_version: str, is_enabled: bool = True):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_roles_packages_endpoint(role_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_packages_to_roles_payload(
                package_id, package_version, is_enabled
            )
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_request(response.request.body)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, \
            (f'Expected status code {HTTPStatus.CREATED}, '
             f'but got {response.status_code}, {data_response}')
        model = SuccessPostRolePackagesModel(results=response.json())
        logger.success(f'Successfully add packages for role ID {role_id}.')
        return model

    @allure.step("Delete packages from role.")
    def delete_roles_packages_by_id(self, role_id: int, *package_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_roles_packages_by_id_endpoint(role_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_packages_from_roles_by_list_payload(*package_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_request(response.request.body)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            (f'Expected status code {HTTPStatus.ACCEPTED}, '
             f'but got {response.status_code}, {data_response}')
        logger.success(f'Successfully delete packages {package_ids} for role ID {role_id}.')
        return response.status_code

    @allure.step("Activate role packages.")
    def put_roles_packages_activate(self, role_id: int, *package_ids: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_roles_packages_activate_endpoint(role_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_activate_packages_roles_by_list_payload(*package_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_request(response.request.body)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            (f'Expected status code {HTTPStatus.ACCEPTED}, '
             f'but got {response.status_code}, {data_response}')
        logger.success(f'Successfully activate packages {package_ids} for role ID {role_id}.')
        return response.status_code

    @allure.step("Deactivate role packages.")
    def put_roles_packages_deactivate(self, role_id: int, *package_ids: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_roles_packages_deactivate_endpoint(role_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_deactivate_packages_roles_by_list_payload(*package_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_request(response.request.body)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            (f'Expected status code {HTTPStatus.ACCEPTED}, '
             f'but got {response.status_code}, {data_response}')
        logger.success(f'Successfully deactivate packages {package_ids} for role ID {role_id}.')
        return response.status_code

    @allure.step("Get list roles packages with range/fetch")
    def get_list_roles_packages_with_range_and_fetch(self, role_id: int):
        start = time.time()
        response_range = requests.get(
            url=self.endpoints.get_list_roles_packages_by_id_endpoint(role_id),
            headers={**self.headers.basic_header(get_token()), "Range": "items=0-1"},
            params={"fetch": "1"}
        )
        end = time.time()
        logger.info(response_range.headers)
        self.attach_response_headers(response_range.headers)
        data_response = self.response_content(response_range)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response_range.request.url)
        assert response_range.status_code == HTTPStatus.PARTIAL_CONTENT, \
            (f'Expected status code {HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response_range.status_code}, {data_response}')
        assert "Content-Range" in response_range.headers, "Response is missing 'Content-Range' header"
        logger.success(f'Successfully get list roles packages with range/fetch.')
        return None

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
        logger.success(f'Successfully get role permissions api {role_id}.')
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
        logger.success(f'Successfully get role permissions ext {role_id}.')
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
        logger.success(f'Successfully get role permissions UI {role_id}.')
        return model
