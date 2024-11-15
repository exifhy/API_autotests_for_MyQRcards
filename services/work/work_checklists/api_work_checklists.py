from requests import JSONDecodeError
import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.work.work_checklists.payloads import Payloads
from services.work.work_checklists.endpoints import Endpoints
from config.headers import Headers
from services.work.work_checklists.models.work_checklists_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from random import randint

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class WorkChecklistsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add checklists.")
    def post_add_checklists(self):
        name = f'Чек-лист-{randint(1, 999)}'
        description = f'Описание-{randint(1, 999)}'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_checklists_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_add_checklists_payload(
                name=name,
                desc=description
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}, {response.json()}'
        model = SuccessAddChecklistsToAssetModel(result=response.json())
        logger.info(f'Successfully add checklists with name {name}.')
        return model

    @allure.step("Delete checklist by ID.")
    def delete_checklist_by_id(self, checklist_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_checklist_by_id_endpoint(checklist_id),
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
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.warning(f'Successfully delete checklist with ID: {checklist_id}.')

