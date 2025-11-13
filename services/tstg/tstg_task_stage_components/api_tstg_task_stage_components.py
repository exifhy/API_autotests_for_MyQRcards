import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.tstg.tstg_task_stage_components.payloads import Payloads
from services.tstg.tstg_task_stage_components.endpoints import Endpoints
from config.headers import Headers
from services.tstg.tstg_task_stage_components.models.tstg_task_stages_components_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class TstgTaskStagesComponentsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add the availability of a component for specified roles at specified stages, capability RW.")
    def post_task_stage_components_rw(self, task_stage_id: int, attribute_id: int, role_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_task_stage_components_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_task_stage_components_rw_payload(task_stage_id, attribute_id, role_id)
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
        logger.info(f'Successfully add the availability of a component {attribute_id} for role id {role_id} at stage id {task_stage_id}.')
        return None