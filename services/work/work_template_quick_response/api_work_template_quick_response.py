import random
import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.work.work_template_quick_response.payloads import Payloads
from services.work.work_template_quick_response.endpoints import Endpoints
from config.headers import Headers
from services.work.work_template_quick_response.models.work_template_quick_response_models import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class WorkTemplateQuickResponseAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get list template quick response.")
    def get_list_template_quick_response(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_template_quick_response_endpoint,
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info("Tenant does not contain template quick response.")
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessTemplateQuickResponseModel(root=response.json())
        logger.info(f'Successfully get template quick response.')
        return model

    @allure.step("Update template quick response.")
    def put_update_template_quick_response(self, response_id: int):
        model_before = self.get_template_quick_response_by_id(response_id)
        data = {
            "id": response_id,
            "name": f"Измененный быстрый ответ - {random.randint(1, 99999)}",
            "riposte": f"Измененное пояснение - {random.randint(1, 99999)}",
            "isTaskTypeAll": True
        }
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_template_quick_response_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.put_template_quick_response_payload(data)
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
        model_after = self.get_template_quick_response_by_id(response_id)
        assert model_before.name != model_after.name, \
            f"Template quick response is not updated. {model_before.name} is equal {model_after.name}"
        assert model_before.riposte != model_after.riposte, \
            f"Template quick response is not updated. {model_before.riposte} is equal {model_after.riposte}"
        logger.info(f'Successfully Update template quick response ID {response_id}.')

    @allure.step("Add template quick response.")
    def post_template_quick_response(self):
        data = {
            "name": f"Быстрый ответ - {random.randint(1, 99999)}",
            "riposte": f"Пояснение - {random.randint(1, 99999)}",
            "isTaskTypeAll": True
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_template_quick_response_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_add_template_quick_response_payload(data)
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
        model = SuccessAddTemplateQuickResponseModel(results=response.json())
        logger.info(f'Successfully add template quick response ID {model.results[0]}.')
        return model

    @allure.step("Add two template quick response.")
    def post_add_two_template_quick_response(self):
        data = {
            "name": f"Быстрый ответ - {random.randint(1, 99999)}",
            "riposte": f"Пояснение - {random.randint(1, 99999)}",
            "isTaskTypeAll": True
        }
        data2 = {
            "name": f"Быстрый ответ - {random.randint(1, 99999)}",
            "riposte": f"Пояснение - {random.randint(1, 99999)}",
            "isTaskTypeAll": True
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_template_quick_response_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_add_template_quick_response_payload(data, data2)
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
        model = SuccessAddTemplateQuickResponseModel(results=response.json())
        logger.info(f'Successfully add two template quick response ID {model.results}.')
        return model

    @allure.step("Delete template quick response by list.")
    def delete_template_quick_response_by_list(self, *response_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_template_quick_response_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_template_quick_response_by_list_payload(*response_ids)
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
        logger.warning(f'Successfully delete template quick response ID {response_ids}.')

    @allure.step("Get template quick response by ID.")
    def get_template_quick_response_by_id(self, response_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_template_quick_response_by_id_endpoint(response_id),
            headers=self.headers.basic_header(API_TOKEN)
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
        model = TemplateQuickResponseListResult(**response.json())
        logger.info(f'Successfully get template quick response by ID {response_id}.')
        return model

    @allure.step("Update bind template quick response and task types.")
    def put_update_task_type_template_quick_response(self, response_id: int, task_type_id: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_task_type_template_quick_response_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.put_update_task_type_template_quick_response_by_list_payload(
                response_id,
                task_type_id
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
        logger.info(f'Successfully update bind template quick response ID {response_id} and task type ID {task_type_id}.')
