import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.work.work_task_order_by.payloads import Payloads
from services.work.work_task_order_by.endpoints import Endpoints
from config.headers import Headers
from services.work.work_task_order_by.models.work_task_order_by_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class WorkTaskOrderByAPI(Helper):
    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get task order by.")
    def get_task_order_by(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_task_order_by_endpoint,
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, f'Status code {response.status_code}, {response.json()}'
        model = SuccessGetTaskOrderByModels(root=response.json())
        logger.info(f'Successfully get task order by.')
        return model

    @allure.step("Get task order by with range.")
    def get_task_order_by_with_range(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_task_order_by_endpoint,
            headers=self.headers.basic_header_with_range(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.PARTIAL_CONTENT, f'Status code {response.status_code}, {response.json()}'
        model = SuccessGetTaskOrderByModels(root=response.json())
        logger.info(f'Successfully get task order by with range.')
        return model
