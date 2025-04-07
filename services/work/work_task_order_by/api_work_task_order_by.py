import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.work.work_task_order_by.payloads import Payloads
from services.work.work_task_order_by.endpoints import Endpoints
from config.headers import Headers
from services.work.work_task_order_by.models.work_task_order_by_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


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
            headers=self.headers.basic_header(get_token())
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
        model = SuccessGetTaskOrderByModels(root=response.json())
        logger.info(f'Successfully get task order by.')
        return model

    @allure.step("Get task order by with range.")
    def get_task_order_by_with_range(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_task_order_by_endpoint,
            headers=self.headers.basic_header_with_range(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.PARTIAL_CONTENT, \
            f'Expected status code {HTTPStatus.PARTIAL_CONTENT}, but got {response.status_code}, {data_response}'
        model = SuccessGetTaskOrderByModels(root=response.json())
        logger.info(f'Successfully get task order by with range.')
        return model
