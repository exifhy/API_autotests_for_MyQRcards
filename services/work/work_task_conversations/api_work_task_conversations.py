import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.work.work_task_conversations.payloads import Payloads
from services.work.work_task_conversations.endpoints import Endpoints
from config.headers import Headers
from services.work.work_task_conversations.models.work_task_conversations_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class WorkTaskConversationsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get list task conversations by task ID.")
    def get_list_task_conversations_by_task_id(self, task_id: int, token: str or None):
        if token is None:
            token = API_TOKEN
        params = {
            "taskID": task_id
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_task_conversations_endpoint, params=params,
            headers=self.headers.basic_header(token)
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
        model = SuccessGetListTaskMessageModel(result=response.json())
        logger.info(f'Successfully get list conversations by task ID: {task_id}.')
        return model

    @allure.step("Get list task conversations.")
    def get_list_task_conversations(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_task_conversations_endpoint,
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
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning(f'{response.status_code}')
        else:
            assert response.status_code == HTTPStatus.OK, f'Status code {response.status_code}, {response.json()}'
            model = SuccessGetListTaskMessageModel(result=response.json())
            logger.info(f'Successfully get list conversations.')
            return model

    @allure.step("Delete task conversations.")
    def delete_task_conversations(self, task_id: int, *message_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_task_conversations_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_task_conversations_payload(
                task_id,
                *message_ids
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
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully delete task conversations with ID: {message_ids}.')

    @allure.step("Head task conversations check count unread message.")
    def head_task_conversations_check_items(self, message_qty: int, token: str or None):
        if token is None:
            token = API_TOKEN
        params = {
            "isRead": False
        }
        start = time.time()
        response = requests.head(
            url=self.endpoints.head_task_conversations_endpoint, params=params,
            headers=self.headers.basic_header(token)
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
        unread_message = int(response.headers['Content-Range'].split('/')[-1])
        assert unread_message == message_qty, \
            f'Expected {message_qty}, but got {unread_message}'
        assert response.status_code == HTTPStatus.OK, \
            f'Status code {response.status_code}, {response.json()}'
        logger.info('Successfully get head task conversations.')

    @allure.step("Head task conversations.")
    def head_task_conversations(self):
        params = {
            "isRead": False
        }
        start = time.time()
        response = requests.head(
            url=self.endpoints.head_task_conversations_endpoint, params=params,
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
        assert response.status_code == HTTPStatus.OK, \
            f'Status code {response.status_code}, {response.json()}'
        logger.info('Successfully get head task conversations.')

    @allure.step("Delete (remove) task conversations.")
    def delete_remove_task_conversations(self, task_id: int, *message_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_remove_task_conversations_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_task_conversations_payload(
                task_id,
                *message_ids
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
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully delete (remove) task conversations with ID: {message_ids}.')
