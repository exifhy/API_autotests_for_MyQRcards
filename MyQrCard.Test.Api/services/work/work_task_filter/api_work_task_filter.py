import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.work.work_task_filter.payloads import Payloads
from services.work.work_task_filter.endpoints import Endpoints
from config.headers import Headers
from services.work.work_task_filter.models.work_task_filter_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class WorkTaskFilterAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get list task filters.")
    def get_list_task_filter(self):
        params = {
            "selectedOnly": False
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_task_filter_endpoint, params=params,
            headers=self.headers.basic_header(get_token())
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
        model = SuccessGetListTaskFilterModel(result=response.json())
        logger.info(f'Successfully get list task filter, selectedOnly=false.')
        return model

    @allure.step("Update task filters.")
    def put_update_task_filters(self, id_: int, attribute_id: bool, sort: int):
        params = {
            "id": id_,
            "isAttribute": attribute_id,
            "sortOrder": sort
        }
        start = time.time()
        response = requests.put(
            url=self.endpoints.get_list_task_filter_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_task_filter_payload(params)
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
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully update list task filter with ID: {id_}.')
