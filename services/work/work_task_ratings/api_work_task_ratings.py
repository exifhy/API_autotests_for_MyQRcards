import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.work.work_task_ratings.payloads import Payloads
from services.work.work_task_ratings.endpoints import Endpoints
from config.headers import Headers
from services.work.work_task_ratings.models.work_task_ratings_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from random import randint

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class WorkTaskRatingsAPI(Helper):
    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add task ratings.")
    def post_task_ratings(self, task_id: int):
        data = {
            "taskID": task_id,
            "ratingCriteriaID": 1,
            "rating": randint(1, 5)
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_task_ratings_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_task_ratings_payload(data)
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
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}. {data_response}'
        logger.info(f'Successfully add task ID {task_id} ratings.')
