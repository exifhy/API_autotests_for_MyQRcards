import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.work.work_task_contacts.payloads import Payloads
from services.work.work_task_contacts.endpoints import Endpoints
from config.headers import Headers
from services.work.work_task_contacts.models.work_task_contacts_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class WorkTaskContactsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Adds contact persons to the task.")
    def post_add_contacts_to_task(self, task_id: int, *contact_ids: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_contacts_to_task_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_contacts_to_task_payload(
                task_id,
                *contact_ids
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
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}, {response.json()}'
        model = SuccessGetListTaskContactsModel(result=response.json())
        logger.info(f'Successfully adds contact with ID: {contact_ids} persons to the task with ID: {task_id}.')
        return model

    @allure.step("Delete contact persons from task.")
    def delete_contacts_from_task(self, task_id: int, *contact_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_contacts_from_task_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_contacts_from_task_payload(
                task_id,
                *contact_ids
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
        logger.info(f'Successfully delete contacts with ID: {contact_ids} persons from task with ID: {task_id}.')
