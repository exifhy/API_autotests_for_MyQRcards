import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.work.work_task_type_routes.payloads import Payloads
from services.work.work_task_type_routes.endpoints import Endpoints
from config.headers import Headers
from services.work.work_task_type_routes.models.work_task_type_routes_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class WorkTaskTypeRoutesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Creates routes of task types.")
    def post_add_task_types_routes(
            self,
            task_type_id: str,
            start_task_stage_id: int,
            start_task_status_id: str,
            finish_task_stage_id: int
    ):
        data = {
            "taskTypeID": task_type_id,
            "startTaskStageID": start_task_stage_id,
            "startTaskStatusID": start_task_status_id,
            "finishTaskStageID": finish_task_stage_id
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_task_type_routes_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_add_task_type_routes_payload(data)
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
        logger.info(f'Successfully creates routes of task types.')

    @allure.step("Update routes task types.")
    def put_update_task_types_routes(
            self,
            task_type_id: str,
            start_task_stage_id: int,
            start_task_status_id: str,
            finish_task_stage_id: int
    ):
        data = {
            "taskTypeID": task_type_id,
            "startTaskStageID": start_task_stage_id,
            "startTaskStatusID": start_task_status_id,
            "finishTaskStageID": finish_task_stage_id
        }
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_task_type_routes_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.put_update_task_type_routes_payload(data)
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
        logger.info(f'Successfully update routes task types.')

    @allure.step("Delete routes task types by list.")
    def delete_task_types_routes_by_list(self, *task_type_routes_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_task_type_routes_by_list_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_task_type_routes_by_list_payload(*task_type_routes_ids)
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
        logger.warning(f'Successfully delete routes task types {task_type_routes_ids} by list.')

    @allure.step("Delete routes task types by ID.")
    def delete_task_types_routes_by_id(self, task_type_routes_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_task_type_routes_by_id_endpoint(task_type_routes_id),
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
        logger.warning(f'Successfully delete routes task types {task_type_routes_id} by ID.')
