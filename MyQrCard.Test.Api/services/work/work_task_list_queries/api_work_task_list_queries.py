import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.work.work_task_list_queries.payloads import Payloads
from services.work.work_task_list_queries.endpoints import Endpoints
from config.headers import Headers
from services.work.work_task_list_queries.models.work_task_list_queries_model import *
import time
from http import HTTPStatus
from random import randint
from utils.token_utils import get_token


class WorkTaskListQueriesAPI(Helper):
    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get list task queries.")
    def get_task_list_queries(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_task_list_queries_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning('NO CONTENT (204)')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessGetTaskListQueryResultModel(root=response.json())
        logger.success(f'Successfully get task list queries.')
        return model

    @allure.step("Add list task queries.")
    def post_task_list_queries(self, district_id: int, work_type_id: int):
        query_name = f'{randint(1000, 99999)}'
        params = (f"districtID={district_id}&isClosed=false&isDeleted=false&orderBy=1&searchText=&"
                  f"sortDirection=2&workTypeID={work_type_id}")
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_task_list_queries_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_task_list_queries_payload(query_name, params)
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
        model = SuccessAddTaskListQueryResultModel(result=response.json())
        logger.success(f'Successfully add task list queries (district, work type).')
        return model

    @allure.step("Add list task queries by owner user.")
    def post_task_list_queries_by_owner_user(self, district_id: int, work_type_id: int, token: str):
        query_name = f'{randint(1000, 99999)}'
        params = (f"districtID={district_id}&isClosed=false&isDeleted=false&orderBy=1&searchText=&"
                  f"sortDirection=2&workTypeID={work_type_id}")
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_task_list_queries_endpoint,
            headers=self.headers.basic_header(token),
            json=self.payloads.post_task_list_queries_payload(query_name, params)
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
        model = SuccessAddTaskListQueryResultModel(result=response.json())
        logger.success(f'Successfully add task list queries (district, work type).')
        return model

    @allure.step("Update list task queries.")
    def put_task_list_queries(self, query_id: int):
        query_name = f'Новый запрос{randint(1, 999)}'
        params = f"isClosed=false&isDeleted=false&orderBy=1&searchText=&sortDirection=2"
        start = time.time()
        response = requests.put(
            url=self.endpoints.post_task_list_queries_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_task_list_queries_payload(query_id, query_name, params)
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
        logger.success(f'Successfully update task list queries.')

    @allure.step("Delete list task queries by list.")
    def delete_task_list_queries_by_list(self, *query_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_task_list_queries_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_task_list_queries_payload(*query_ids)
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
        logger.success(f'Successfully delete task list queries by list with IDs: {query_ids}.')

    @allure.step("Delete list task queries by list by owner user.")
    def delete_task_list_queries_by_list_by_owner_user(self, token: str,  *query_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_task_list_queries_endpoint,
            headers=self.headers.basic_header(token),
            json=self.payloads.delete_task_list_queries_payload(*query_ids)
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
        logger.success(f'Successfully delete task list queries by list with IDs: {query_ids}.')

    @allure.step("Delete list task queries by list (remove).")
    def delete_remove_task_list_queries_by_list(self, *query_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_remove_task_list_queries_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_remove_task_list_queries_payload(*query_ids)
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
        logger.success(f'Successfully delete task list queries by list with IDs: {query_ids}.')

    @allure.step("Get list task queries by id.")
    def get_task_list_queries_by_id(self, query_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_task_list_queries_by_id_endpoint(query_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = TaskListQueryResultModel(**response.json())
        logger.success(f'Successfully get task list queries with ID: {query_id}.')
        return model

    @allure.step("Delete list task queries by id.")
    def delete_task_list_queries_by_id(self, query_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_task_list_queries_by_id_endpoint(query_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        model_list = self.get_task_list_queries()
        if model_list is None:
            logger.success(f'Successfully delete task list queries with ID: {query_id}.')
        else:
            assert str(query_id) not in model_list.root, \
                f'Task list queries with id {query_id} not deleted.'
            logger.success(f'Successfully delete task list queries with ID: {query_id}.')

    @allure.step("Delete list task queries by id (remove).")
    def delete_task_list_queries_by_id_remove(self, query_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_remove_task_list_queries_by_id_endpoint(query_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.success(f'Successfully delete (remove) task list queries with ID: {query_id}.')
