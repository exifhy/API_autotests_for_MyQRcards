import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.work.work_task_attributes.payloads import Payloads
from services.work.work_task_attributes.endpoints import Endpoints
from config.headers import Headers
from services.work.work_task_attributes.models.work_task_attributes_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class WorkTaskAttributesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Changes attribute values on task.")
    def post_add_task_attributes(self, attribute_id: int, task_id: int):
        value = f"Значение дополнительного поля."
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_task_attributes_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_add_task_attributes_payload(
                task_id=task_id,
                attribute_id=attribute_id,
                value=value
            )
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
        logger.info(f'Successfully changes attribute values on task with ID: {task_id}.')

    @allure.step("Returns attribute values by task.")
    def get_list_task_attributes(self, attribute_id: int, task_id: int):
        params = {
            "taskID": task_id,
            "attributeID": attribute_id
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_task_attributes_endpoint, params=params,
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
        model = SuccessGetListTaskAttributesResultModel(result=response.json())
        logger.info(f'Successfully returns attribute with ID: {attribute_id} values by task with ID: {task_id}.')
        return model
