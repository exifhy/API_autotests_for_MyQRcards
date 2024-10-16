from datetime import datetime, timezone, timedelta
import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.work.work_task_assignment_history.payloads import Payloads
from services.work.work_task_assignment_history.endpoints import Endpoints
from config.headers import Headers
from services.work.work_task_assignment_history.models.work_task_assiggnment_history_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class WorkTaskAssignmentHistoryAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add new task to a user.")
    def post_add_new_task_to_user(self, user_id: int, task_id: int):
        current_time = datetime.now(timezone.utc)
        date_start_iso = current_time.isoformat(timespec='milliseconds')
        date_start = date_start_iso.replace('+00:00', 'Z')
        date_tomorrow = current_time + timedelta(1)
        date_end_iso = date_tomorrow.isoformat(timespec='milliseconds')
        date_end = date_end_iso.replace('+00:00', 'Z')
        start = time.time()
        response = requests.post(
            url=self.endpoints.add_new_task_to_user_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.add_new_task_assignment_history(
                user_id=user_id,
                task_id=task_id,
                date_start=date_start,
                date_end=date_end
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}, {response.json()}'
        model = SuccessAddTaskAssignmentHistoryModel(history=response.json())
        assert model.history[0].taskID == task_id, f'Expected {task_id}, but got {model.history[0].taskID}'
        assert model.history[0].assignments[0].userID == user_id, f'Expected {user_id}, but got {model.history[0].assignments[0].userID}'
        logger.info(f'Successfully add new task to a user.')
        return model
