import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.export.tasks.payloads import Payloads
from services.export.tasks.endpoints import Endpoints
from config.headers import Headers
from services.export.tasks.models.export_tasks_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class ExportTasksAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Returns a list of data available for advanced exports.")
    def get_extended_tasks(self):
        # params = {
        #     "Range": "",
        #     "offset": ""
        # }
        start = time.time()
        response = requests.get(
            url=self.endpoints.export_list_tasks_extended_endpoint,
            headers=self.headers.export_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        logger.warning(response.request.url)
        self.attach_time(start, end)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, f'Status code {response.status_code}'
        model = SuccessTasksResultModel(list=response.json())
        logger.info(f'Successfully get a list of data available for advanced exports.')
        return model
