import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.work.work_task_type_district.payloads import Payloads
from services.work.work_task_type_district.endpoints import Endpoints
from config.headers import Headers
from services.work.work_task_type_district.models.work_task_type_district_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class WorkTaskTypeDistrictAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Changing the binding of task types to district.")
    def put_update_task_type_district(self, task_type_id: int, *district_ids: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_task_type_district_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.put_update_task_type_district_payload(
                task_type_id,
                *district_ids
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
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.info(f'Successfully changing the binding of task types {task_type_id} to district {district_ids}.')
