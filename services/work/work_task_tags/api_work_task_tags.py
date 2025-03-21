import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.work.work_task_tags.payloads import Payloads
from services.work.work_task_tags.endpoints import Endpoints
from config.headers import Headers
from services.work.work_task_tags.models.work_task_tags_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from random import randint


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class WorkTaskTagsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add tags to task.")
    def post_add_tags_to_task(self, task_id: int):
        tags = f"tag-{randint(1, 9999)}"
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_task_tags_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_task_tags_payload(
                task_id,
                tags
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
        logger.info(f'Successfully add tags <{tags}> task ID {task_id}')
        return tags

    @allure.step("Delete tags from task.")
    def delete_tags_from_task(self, task_id: int, tags: str):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_task_tags_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_task_tags_payload(
                task_id,
                tags
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
        logger.warning(f'Successfully delete tags <{tags}> from task ID {task_id}')
