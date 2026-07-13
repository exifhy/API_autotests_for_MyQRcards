from requests import JSONDecodeError
import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.work.work_request_methods.payloads import Payloads
from services.work.work_request_methods.endpoints import Endpoints
from config.headers import Headers
from services.work.work_request_methods.models.work_request_methods_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class WorkRequestMethodsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get list request methods orders task.")
    def get_request_methods(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_request_methods_endpoint,
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
        model = SuccessRequestMethodsListResultModel(root=response.json())
        logger.info(f'Successfully get list request methods orders task.')
        return model
