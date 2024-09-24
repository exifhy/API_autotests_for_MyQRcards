import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.common.common_applications.payloads import Payloads
from services.common.common_applications.endpoints import Endpoints
from config.headers import Headers
from services.common.common_applications.models.common_applications_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
APP_ID = os.getenv('APP_ID')


class CommonApplicationsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Returns a list of branches.")
    def get_list_applications(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_of_branches_endpoint,
            headers=self.headers.auth_header(bearer_token=API_TOKEN, app_id=APP_ID)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, f'Status code {response.status_code}'
        model = SuccessGetApplicationResultModel(root=response.json())
        logger.warning(f'Successfully received list of branches (applications).')
        return model
