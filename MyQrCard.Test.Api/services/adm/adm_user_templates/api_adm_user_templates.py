import random
import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.adm.adm_user_templates.payloads import Payloads
from services.adm.adm_user_templates.endpoints import Endpoints
from config.headers import Headers
from services.adm.adm_user_templates.models.adm_user_templates_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class AdmUserTemplatesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get list user templates.")
    def get_list_user_templates(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_user_templates_endpoint,
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list of user templates.")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}, {data_response}')
        model = SuccessGetUserTemplatesListResultModel(root=response.json())
        logger.info(f'Successfully get user templates.')
        return model

    @allure.step("Get user template by id.")
    def get_user_template_by_id(self, template_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_user_template_endpoint(template_id),
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
        model = UserTemplateGetResult(**response.json())
        logger.info(f'Successfully get user template by id {template_id}.')
        return model

    @allure.step("Add user template.")
    def post_add_user_template(self):
        name = f"Шаблон-{random.randint(1, 9999)}"
        data = {
            "name": name,
            "isCustomer": True,
            "isTechnician": False,
            "isTeam": False
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_user_templates_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_user_template_payload(data)
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
        model = SuccessAddUserTemplatesModel(results=response.json())
        logger.info(f'Successfully add user template ID {model.results[0]}.')
        return model

    @allure.step("Add three user templates.")
    def post_add_three_user_templates(self):
        data = {
            "name": f"Шаблон-{random.randint(9999, 99999)}",
            "isCustomer": True,
            "isTechnician": False,
            "isTeam": False
        }
        data2 = {
            "name": f"Шаблон-{random.randint(99999, 999999)}",
            "isCustomer": True,
            "isTechnician": False,
            "isTeam": False
        }
        data3 = {
            "name": f"Шаблон-{random.randint(999999, 9999999)}",
            "isCustomer": True,
            "isTechnician": False,
            "isTeam": False
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_user_templates_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_user_template_payload(data, data2, data3)
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
        model = SuccessAddUserTemplatesModel(results=response.json())
        logger.info(f'Successfully add three user templates {model.results[0], model.results[1], model.results[2]}.')
        return model

    @allure.step("Update user template.")
    def put_update_user_template(self, template_id: int):
        model_before = self.get_user_template_by_id(template_id)
        name = f"Измененный шаблон-{random.randint(1, 9999)}"
        data = {
            "id": template_id,
            "name": name,
            "isCustomer": True,
            "isTechnician": False,
            "isTeam": False
        }
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_user_templates_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_user_template_payload(data)
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
        model_after = self.get_user_template_by_id(template_id)
        assert model_before.name != model_after.name, f"{model_before.name} is equal {model_after.name}"
        logger.info(f'Successfully update user template ID {template_id}.')
        return None

    @allure.step("Delete user template by ID.")
    def delete_user_template_by_id(self, template_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_user_template_endpoint(template_id),
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.warning(f'Successfully delete user template ID {template_id}.')

    @allure.step("Delete user templates by list.")
    def delete_user_templates_by_list(self, *template_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_user_templates_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_user_templates_by_list_payload(*template_ids)
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
        logger.warning(f'Successfully delete user template IDs {template_ids}.')

    @allure.step("Get districts user template by id.")
    def get_districts_user_template_by_id(self, template_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_user_templates_districts(template_id),
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
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list of districts user template.")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}, {data_response}')
        model = SuccessGetUserTemplatesListResultDistrictsModel(results=response.json())
        logger.info(f'Successfully get districts user template by id {template_id}.')
        return model

    @allure.step("Get roles user template by id.")
    def get_roles_user_template_by_id(self, template_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_user_templates_roles(template_id),
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
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list of roles user template.")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}, {data_response}')
        model = SuccessGetUserTemplatesRolesModel(results=response.json())
        logger.info(f'Successfully get roles user template by id {template_id}.')
        return model
