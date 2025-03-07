import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.work.work_task_watch_lists.payloads import Payloads
from services.work.work_task_watch_lists.endpoints import Endpoints
from config.headers import Headers
from services.work.work_task_watch_lists.models.work_task_watch_lists_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from random import randint


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class WorkTaskWatchListsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add watch lists to task.")
    def post_add_watch_lists_to_task(self, task_id: int, user_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_task_watch_lists_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_add_task_watch_lists_payload(
                task_id,
                user_id
            )
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessAddTaskWatchListsModel(results=response.json())
        logger.info(f'Successfully add watch lists ID <{user_id}> to task ID {task_id}')
        return model

    @allure.step("Delete watch lists from task.")
    def delete_tags_from_task(self, task_id: int, user_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_task_watch_lists_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_task_watch_lists_payload(
                task_id,
                user_id
            )
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.info(f'Successfully delete watch lists ID <{user_id}> from task ID {task_id}')
