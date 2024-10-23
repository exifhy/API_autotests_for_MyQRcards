import random
import allure
import requests
from datetime import timezone, datetime
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.work.work_task_types.payloads import Payloads
from services.work.work_task_types.endpoints import Endpoints
from config.headers import Headers
from services.work.work_task_types.models.work_task_types_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class WorkTaskTypesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get list task types and returns ID the first existing.")
    def get_list_task_types_return_first_id(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_task_types_endpoint,
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, f'Status code {response.status_code}, {response.json()}'
        model = SuccessGetListTaskTypesModel(root=response.json())
        for key, value in model.root.items():
            logger.info(f'Successfully get list task types.')
            logger.info(f'Task type ID: {key}, name: {value.name}')
            return key

    @allure.step("Get list task types.")
    def get_list_task_types(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_task_types_endpoint,
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, f'Status code {response.status_code}, {response.json()}'
        model = SuccessGetListTaskTypesModel(root=response.json())
        logger.info(f'Successfully get list a task types.')
        return model
