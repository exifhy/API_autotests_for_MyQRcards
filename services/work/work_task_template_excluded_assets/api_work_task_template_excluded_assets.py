import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.work.work_task_template_excluded_assets.payloads import Payloads
from services.work.work_task_template_excluded_assets.endpoints import Endpoints
from config.headers import Headers
from services.work.work_task_template_excluded_assets.models.work_task_template_excluded_assets_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class WorkTaskTemplateExcludedAssetsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add task template excluded assets.")
    def post_task_template_excluded_assets(self, task_template_id: str, *asset_ids: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_task_template_excluded_assets_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_add_task_template_excluded_assets_payload(
                task_template_id,
                *asset_ids
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
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessListTaskTemplateExcludedAssetsModel(results=response.json())
        logger.info(f'Successfully add task template {task_template_id} excluded assets {asset_ids}.')
        return model

    @allure.step("Delete task template excluded assets.")
    def delete_task_template_excluded_assets(self, task_template_id: str, *asset_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_task_template_excluded_assets_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_task_template_excluded_assets_payload(
                task_template_id,
                *asset_ids
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
        logger.warning(f'Successfully delete task template ID {task_template_id} excluded assets {asset_ids}.')
