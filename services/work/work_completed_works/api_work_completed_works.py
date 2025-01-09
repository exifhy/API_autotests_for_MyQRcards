from requests import JSONDecodeError
import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.work.work_completed_works.payloads import Payloads
from services.work.work_completed_works.endpoints import Endpoints
from config.headers import Headers
from services.work.work_completed_works.models.work_completed_works_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from random import randint
from datetime import datetime, timedelta

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class WorkCompletedWorksAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Creates completed work on task.")
    def post_add_completed_works(self, task_id: int, asset_id: int, work_type_id: int):
        description = f'Комментарий к выполненной работе-{randint(1, 999)}'
        current_time = datetime.now()
        time_delta_start = current_time - timedelta(minutes=5)
        date_start = time_delta_start.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-4]
        date_end = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-4]
        data = {
            "maintainedAssetID": asset_id,
            "workTypeID": work_type_id,
            "started": date_start,
            "finished": date_end,
            "notes": description
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_completed_works_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_add_completed_works_payload(task_id, data)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}, {response.json()}'
        model = SuccessAddCompletedWorksModel(result=response.json())
        logger.info(f'Successfully creates completed work on task with ID: {model.result[0].id}.')
        return model

    @allure.step("Update completed work on task.")
    def put_update_completed_works(self, completed_work_id: int, task_id: int, asset_id: int, work_type_id: int):
        description = f'Обновленный комментарий к выполненной работе-{randint(1, 999)}'
        current_time = datetime.now()
        time_delta_start = current_time - timedelta(minutes=10)
        date_start = time_delta_start.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-4]
        date_end = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-4]
        data = {
            "id": completed_work_id,
            "maintainedAssetID": asset_id,
            "workTypeID": work_type_id,
            "started": date_start,
            "finished": date_end,
            "notes": description
        }
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_completed_works_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.put_update_completed_works_payload(task_id, data)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully update completed work on task with ID: {completed_work_id}.')

    @allure.step("Delete completed work from task by list.")
    def delete_completed_works_by_list(self, *completed_work_ids: int, task_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_completed_works_by_list_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_completed_works_by_list_payload(*completed_work_ids, task_id=task_id)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully delete completed works from task with ID: {completed_work_ids}.')
