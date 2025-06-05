import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.adm.adm_user_task_list_queries.payloads import Payloads
from services.adm.adm_user_task_list_queries.endpoints import Endpoints
from config.headers import Headers
from services.adm.adm_user_task_list_queries.models.adm_user_task_list_queries_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class AdmUserTaskListQueriesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add user task list queries.")
    def post_add_user_task_list_queries(self, user_id: int, *task_list_queries_ids: int or tuple):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_user_task_list_queries_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_user_task_list_queries_payload(user_id, *task_list_queries_ids)
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
            (f'Expected status code {HTTPStatus.CREATED}, '
             f'but got {response.status_code}, {data_response}')
        model = UserTaskListQueriesResponseModel(results=response.json())
        logger.info(f'Successfully add user ID {user_id} task list queries ID {task_list_queries_ids}.')
        return model

    @allure.step("Delete user task list queries.")
    def delete_user_task_list_queries(self, user_id: int, *task_list_queries_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_user_task_list_queries_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_user_task_list_queries_payload(user_id, *task_list_queries_ids)
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
            (f'Expected status code {HTTPStatus.ACCEPTED}, '
             f'but got {response.status_code}, {data_response}')
        logger.warning(f'Successfully delete task list queries ID {task_list_queries_ids} from user ID {user_id}.')
        return None
