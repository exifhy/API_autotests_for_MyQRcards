from requests import JSONDecodeError
import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.work.work_task_actualities.payloads import Payloads
from services.work.work_task_actualities.endpoints import Endpoints
from config.headers import Headers
from services.work.work_task_actualities.models.work_task_actualities_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class WorkTaskActualitiesAPI(Helper):
    """Остальные ручки не используются"""

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get list task actualities.")
    def get_list_task_actualities(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_task_actualities_endpoint,
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, f'Status code {response.status_code}, {response.json()}'
        model = SuccessGetListTaskActualitiesModel(root=response.json())
        logger.info(f'Successfully get list task actualities.')
        return model
