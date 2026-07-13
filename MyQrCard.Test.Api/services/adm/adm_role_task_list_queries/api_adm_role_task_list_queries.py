import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.adm.adm_role_task_list_queries.payloads import Payloads
from services.adm.adm_role_task_list_queries.endpoints import Endpoints
from config.headers import Headers
from services.adm.adm_role_task_list_queries.models.adm_role_task_list_queries_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token
from utils.env import get_app_id


class AdmRoleTaskListQueriesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add stored task list queries for a role.")
    def post_role_task_list_queries(self, role_id: int, *task_List_query_id: int | tuple):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_role_task_list_queries_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_role_task_list_queries_payload(
                role_id,
                *task_List_query_id
            )
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
        model = SuccessPostRoleTaskListQueriesModel(results=response.json())
        logger.success(f'Successfully add role ID {role_id} task list queries ID {task_List_query_id}.')
        return model

    @allure.step("Delete stored task list queries from a role.")
    def delete_role_task_list_queries(self, role_id: int, *task_List_query_id: int | tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_role_task_list_queries_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_role_task_list_queries_payload(
                role_id,
                *task_List_query_id
            )
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
        logger.success(f'Successfully delete ID {role_id} task list queries ID {task_List_query_id}.')
        return None

    @allure.step("Verify post role task list queries invalid payload([]).")
    def post_role_task_list_queries_invalid_payload(self):
        start = time.time()
        response_invalid = requests.post(
            url=self.endpoints.post_role_task_list_queries_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=[]
        )
        end = time.time()
        logger.info(response_invalid.headers)
        self.attach_response_headers(response_invalid.headers)
        data_response = self.response_content(response_invalid)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response_invalid.request.body)
        self.attach_url(response_invalid.request.url)
        assert response_invalid.status_code == HTTPStatus.CONFLICT, \
            (f'Expected status code {HTTPStatus.CONFLICT}, '
             f'but got {response_invalid.status_code}, {data_response}')
        model = ErrorModel(list_model=response_invalid.json())
        assert model.list_model[0].message == "Параметр [data] не может быть пустым.", \
            f'Expected message error "Параметр [data] не может быть пустым.", but got {model.list_model[0].message}'
        logger.success("Successfully verify post role task list queries invalid payload.")
        return None

    @allure.step("Verify post role task list queries without auth")
    def post_role_task_list_queries_without_auth(self):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_role_task_list_queries_endpoint,
            headers=self.headers.without_authorization_field_header(get_app_id())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, \
            (f'Expected status code {HTTPStatus.UNAUTHORIZED}, '
             f'but got {response.status_code}, {data_response}')
        logger.success(f'Successfully verify post role task list queries without auth.')
        return None
        
    @allure.step("Verify post role task list queries with invalid app id.")
    def post_role_task_list_queries_invalid_app_id(self):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_role_task_list_queries_endpoint,
            headers=self.headers.auth_header(get_token(), "invalid app id"),
            json=[]
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            (f'Expected status code {HTTPStatus.FORBIDDEN}, '
             f'but got {response.status_code}, {data_response}')
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].message == "Не найден обязательный заголовок [X-Application-ID].", \
            f'Expected message "Не найден обязательный заголовок [X-Application-ID].", but got {model.list_model[0].message}'
        logger.success(f'Successfully verify post role task list queries without invalid app id.')
        return None

    @allure.step("Verify delete role task list queries invalid payload ([])")
    def delete_role_task_list_queries_invalid_payload(self):
        start = time.time()
        response_invalid = requests.delete(
            url=self.endpoints.delete_role_task_list_queries_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=[]
        )
        end = time.time()
        logger.info(response_invalid.headers)
        self.attach_response_headers(response_invalid.headers)
        data_response = self.response_content(response_invalid)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response_invalid.request.body)
        self.attach_url(response_invalid.request.url)
        model = ErrorModel(list_model=response_invalid.json())
        assert model.list_model[0].message == "Параметр [data] не может быть пустым.", \
            f'Expected message error "Параметр [data] не может быть пустым.", but got {model.list_model[0].message}'
        logger.success("Successfully verify delete role task list queries invalid payload.")
        return None

    @allure.step("Verify delete role task list queries without auth")
    def delete_role_task_list_queries_without_auth(self):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_role_task_list_queries_endpoint,
            headers=self.headers.without_authorization_field_header(get_app_id())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, \
            (f'Expected status code {HTTPStatus.UNAUTHORIZED}, '
             f'but got {response.status_code}, {data_response}')
        logger.success(f'Successfully verify delete role task list queries without auth.')
        return None

    @allure.step("Verify delete role task list queries with invalid app id")
    def delete_role_task_list_queries_invalid_app_id(self):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_role_task_list_queries_endpoint,
            headers=self.headers.auth_header(get_token(), "invalid app id"),
            json=[]
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_request(response.request.body)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            (f'Expected status code {HTTPStatus.FORBIDDEN}, '
             f'but got {response.status_code}, {self.response_content(response)}')
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].message == "Не найден обязательный заголовок [X-Application-ID].", \
            f'Expected message "Не найден обязательный заголовок [X-Application-ID].", but got {model.list_model[0].message}'
        logger.success(f'Successfully verify delete role task list queries without invalid app id.')
        return None
