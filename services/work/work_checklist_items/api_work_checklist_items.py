from requests import JSONDecodeError
import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.work.work_checklist_items.payloads import Payloads
from services.work.work_checklist_items.endpoints import Endpoints
from config.headers import Headers
from services.work.work_checklist_items.models.work_checklist_items_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from random import randint

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class WorkChecklistItemsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add checklist items.")
    def post_add_checklist_items(self, checklist_id: int):
        data = {
            "name": f'Пункт-{randint(1, 999)}',
            "description": f'Описание-{randint(1, 999)}',
            "attributeID": None,
            "sortOrder": 0
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_checklist_items_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_add_checklist_items_payload(
                checklist_id,
                data
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
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        model = SuccessAddChecklistItemsModel(result=response.json())
        logger.info(f'Successfully add checklist items.')
        return model

    @allure.step("Delete checklist items.")
    def delete_checklist_items(self, checklist_id: int, checklist_item_id: int):
        data = {
            "checkListID": checklist_id,
            "id": checklist_item_id
        }
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_checklist_items_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_checklist_items_payload(
                data
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
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.warning(f'Successfully delete checklist items.')
