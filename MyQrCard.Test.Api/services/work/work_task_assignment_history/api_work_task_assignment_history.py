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
from utils.token_utils import get_token


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
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.add_new_task_assignment_history(
                user_id=user_id,
                task_id=task_id,
                date_start=date_start,
                date_end=date_end
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
        assert response.status_code == HTTPStatus.CREATED, f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessAddTaskAssignmentHistoryModel(history=response.json())
        assert model.history[0].taskID == task_id, f'Expected {task_id}, but got {model.history[0].taskID}'
        assert model.history[0].assignments[0].userID == user_id, \
            f'Expected {user_id}, but got {model.history[0].assignments[0].userID}'
        logger.success(f'Successfully add new task ID {model.history[0].taskID} '
                    f'to a user ID {model.history[0].assignments[0].userID}.')
        return model

    @allure.step("Add new task to a user fixed date end.")
    def post_add_new_task_to_user_date_end(self, user_id: int, task_id: int):
        current_time = datetime.now(timezone.utc)
        date_start_iso = current_time.isoformat(timespec='milliseconds')
        date_start = date_start_iso.replace('+00:00', 'Z')
        date_tomorrow = current_time + timedelta(1)
        start = time.time()
        response = requests.post(
            url=self.endpoints.add_new_task_to_user_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.add_new_task_assignment_history_payload(
                user_id=user_id,
                task_id=task_id,
                date_start=date_start,
                date_end="2099-12-31T23:30:00.000Z"
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
        assert response.status_code == HTTPStatus.CREATED, f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessAddTaskAssignmentHistoryModel(history=response.json())
        assert model.history[0].taskID == task_id, f'Expected {task_id}, but got {model.history[0].taskID}'
        assert model.history[0].assignments[0].userID == user_id, \
            f'Expected {user_id}, but got {model.history[0].assignments[0].userID}'
        logger.success(f'Successfully add new task ID {model.history[0].taskID} '
                    f'to a user ID {model.history[0].assignments[0].userID}.')
        return model
