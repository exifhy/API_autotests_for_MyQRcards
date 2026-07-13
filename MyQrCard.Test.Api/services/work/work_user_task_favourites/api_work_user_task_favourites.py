import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.work.work_user_task_favourites.payloads import Payloads
from services.work.work_user_task_favourites.endpoints import Endpoints
from config.headers import Headers
from services.work.work_user_task_favourites.models.work_user_task_favourites_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class WorkUserTaskFavouritesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Adds task to the favorites list for the current user.")
    def post_add_task_to_favourite_list_user(self, *task_ids: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_user_task_favourites_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_user_task_favourites_payload(*task_ids)
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
        logger.info(f'Successfully adds task ID {task_ids} to the favorites list for the current user.')

    @allure.step("Delete task from the favorites list the current user.")
    def delete_task_from_favourite_list_user(self, *task_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_user_task_favourites_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_task_from_user_favourites_payload(*task_ids)
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
        logger.warning(f'Successfully delete task ID {task_ids} from the favorites list the current user.')
