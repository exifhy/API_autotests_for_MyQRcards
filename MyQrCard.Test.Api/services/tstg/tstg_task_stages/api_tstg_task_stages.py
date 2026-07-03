import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.tstg.tstg_task_stages.payloads import Payloads
from services.tstg.tstg_task_stages.endpoints import Endpoints
from config.headers import Headers
from services.tstg.tstg_task_stages.models.tstg_task_stages_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class TstgTaskStagesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get list task stages in tenant.")
    def get_list_task_stages_in_tenant(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_task_stages_in_tenant_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessGetListTaskStagesResultModel(**response.json())
        logger.info(f'Successfully get list task stages in tenant')
        return model

    @allure.step("Get list task stages in tenant and return <Новая>.")
    def get_list_task_stages_in_tenant_return_new_id(self) -> int:
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_task_stages_in_tenant_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessGetListTaskStagesResultModel(**response.json())
        for key, stage in model.root.items():
            if stage.name == "Новая":
                logger.info(f'Successfully get list task stages in tenant and return id stage <Новая> {stage.id}')
                return stage.id
