import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.work.work_task_conversation_deliveries.payloads import Payloads
from services.work.work_task_conversation_deliveries.endpoints import Endpoints
from config.headers import Headers
from services.work.work_task_conversation_deliveries.models.work_task_conversation_deliveries_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class WorkTaskConversationDeliveriesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Read conversation deliveries task.")
    def put_task_conversation_deliveries(self, task_id: int, conversation_id: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_task_conversation_deliveries_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.put_task_conversation_deliveries_payload(
                task_id,
                conversation_id
            )
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_request(response.request.body)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.info(f'Successfully read conversation with ID: {conversation_id} deliveries task with ID: {task_id}.')
