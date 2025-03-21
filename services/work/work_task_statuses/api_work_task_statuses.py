import random

import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.work.work_task_statuses.payloads import Payloads
from services.work.work_task_statuses.endpoints import Endpoints
from config.headers import Headers
from services.work.work_task_statuses.models.work_task_statuses_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from random import randint


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class WorkTaskStatusesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add task status.")
    def post_add_task_statuses(self):
        colors = ["FF4500", "6A5ACD", "32CD32", "FFD700", "8A2BE2"]
        value = {
            "name": f"Статус-{randint(1, 999)}",
            "sortOrder": 0,
            "color": f"{random.choice(colors)}"
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_task_statuses_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_add_task_statuses_payload(
                value
            )
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessAddWorkTaskStatusesModel(status=response.json())
        logger.info(f'Successfully add a task status ID {model.status[0]}')
        return model

    @allure.step("Get list task statuses.")
    def get_list_task_statuses(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_task_statuses_endpoint,
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
            logger.warning("No available task statuses")
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessGetListWorkTaskStatusesModel(root=response.json())
        logger.info(f'Successfully get list task statuses')
        return model

    @allure.step("Update task status.")
    def put_update_task_status(self, task_status_id: int):
        colors = ["FF4500", "6A5ACD", "32CD32", "FFD700", "8A2BE2"]
        model_task_status_before = self.get_task_status_by_id(task_status_id)
        value = {
            "id": task_status_id,
            "name": f"Обновленный статус-{randint(1, 999)}",
            "sortOrder": 0,
            "color": f"{random.choice(colors)}"
        }
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_task_statuses_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.put_update_task_statuses_payload(
                value
            )
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        model_task_status_after = self.get_task_status_by_id(task_status_id)
        assert model_task_status_after.name != model_task_status_before, \
            f'{model_task_status_after.name} is equal {model_task_status_before.name}'
        assert model_task_status_after.color != model_task_status_before.color, \
            f'{model_task_status_after.color} is equal {model_task_status_before.color}'
        logger.info(f'Successfully update task status ID {task_status_id}')

    @allure.step("Delete task statuses by list.")
    def delete_task_statuses_by_list(self, *task_statuses_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_task_statuses_by_list_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_task_statuses_by_list_payload(
                *task_statuses_ids
            )
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.warning(f'Successfully delete task statuses ID {task_statuses_ids}')

    @allure.step("Get task status by ID.")
    def get_task_status_by_id(self, task_status_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_task_statuses_by_id_endpoint(task_status_id),
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
        model = WorkTaskStatusesModel(**response.json())
        logger.info(f'Successfully get task status ID {task_status_id}')
        return model

    @allure.step("Delete task status by ID.")
    def delete_task_status_by_id(self, task_status_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_task_statuses_by_id_endpoint(task_status_id),
            headers=self.headers.basic_header(API_TOKEN)
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
        logger.warning(f'Successfully delete task status ID {task_status_id}')
