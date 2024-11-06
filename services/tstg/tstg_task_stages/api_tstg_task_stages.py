import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.tstg.tstg_task_stages.payloads import Payloads
from services.tstg.tstg_task_stages.endpoints import Endpoints
from config.headers import Headers
from services.tstg.tstg_task_stages.models.tstg_task_stages_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


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
        model = SuccessGetListTaskStagesResultModel(**response.json())
        logger.info(f'Successfully get list task stages in tenant')
        return model
