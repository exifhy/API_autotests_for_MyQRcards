import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.work.work_task_skills.payloads import Payloads
from services.work.work_task_skills.endpoints import Endpoints
from config.headers import Headers
from services.work.work_task_skills.models.work_task_skills_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class WorkTaskSkillsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add skills to task.")
    def post_add_skills_to_task(self, task_id: int, *skill_ids: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_task_skills_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_task_skills_payload(
                task_id,
                *skill_ids
            )
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response_headers(response.headers)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessAddWorkTaskSkillsModel(results=response.json())
        logger.info(f'Successfully add skills ID: {model.results[0].skillID} to tasK ID {model.results[0].taskID}.')
        return model

    @allure.step("Delete skills from task.")
    def delete_skills_from_task(self, task_id: int, *skill_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_task_skills_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_task_skills_payload(
                task_id,
                *skill_ids
            )
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response_headers(response.headers)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.warning(f'Successfully delete skills ID: {skill_ids} from tasK ID {task_id}.')
