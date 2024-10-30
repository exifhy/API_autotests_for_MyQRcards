import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.work.work_task_staging_history.payloads import Payloads
from services.work.work_task_staging_history.endpoints import Endpoints
from config.headers import Headers
from services.work.work_task_staging_history.models.work_task_staging_history_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class WorkTaskStagingHistoryAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Adds actual record to the history of the task progress by stage.")
    def post_add_task_staging_history(self, stage_id: str, task_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.add_actual_record_to_history_progress_task_by_stage_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.add_actual_record_to_history_progress_task_by_stage_payload(
                stage_id=stage_id,
                task_id=task_id
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully add task staging history, stage id: {stage_id}.')

    @allure.step("Mass movement of task by stages.")
    def post_multiple_add_task_staging_history(self, stage_id: str, task_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.mass_movement_of_task_by_stage_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.mass_movement_of_task_by_stage_payload(
                stage_id=stage_id,
                task_id=task_id
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}, {response.json()}'
        model = SuccessTaskStagingHistoryModel(history=response.json())
        logger.warning(f'Successfully mass movement of task by stages.')
        return model
