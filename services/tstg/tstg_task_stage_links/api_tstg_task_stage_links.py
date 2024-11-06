import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.tstg.tstg_task_stage_links.payloads import Payloads
from services.tstg.tstg_task_stage_links.endpoints import Endpoints
from config.headers import Headers
from services.tstg.tstg_task_stage_links.models.tstg_task_stage_links_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class TstgTaskStageLinksAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get list task stage links in tenant.")
    def get_list_task_stage_links_in_tenant(self, task_type_id: int, task_stage_from_id: int):
        params = {
            "taskTypeID": task_type_id,
            "taskStageFromID": task_stage_from_id
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_task_stage_links_endpoint, params=params,
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
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            f'Status code {response.status_code}, {response.json()}'
        model = SuccessGetListTaskStageLinksModel(links=response.json())
        logger.info(f'Successfully get list task stage links in tenant.')
        return model
