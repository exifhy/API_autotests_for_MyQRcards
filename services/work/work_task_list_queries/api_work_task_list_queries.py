import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.work.work_task_list_queries.payloads import Payloads
from services.work.work_task_list_queries.endpoints import Endpoints
from config.headers import Headers
from services.work.work_task_list_queries.models.work_task_list_queries_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from random import randint

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


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
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, f'Status code {response.status_code}, {response.json()}'
        model = SuccessGetTaskListQueryResultModel(root=response.json())
        logger.info(f'Successfully get task list queries.')
        return model

    @allure.step("Add list task queries.")
    def post_task_list_queries(self, district_id: int, work_type_id: int):
        query_name = f'{randint(1000, 99999)}'
        params = (f"districtID={district_id}&isClosed=false&isDeleted=false&orderBy=1&searchText=&"
                  f"sortDirection=2&workTypeID={work_type_id}")
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_task_list_queries_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_task_list_queries_payload(query_name, params)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}, {response.json()}'
        model = SuccessAddTaskListQueryResultModel(result=response.json())
        logger.info(f'Successfully add task list queries (district, work type).')
        return model

    @allure.step("Update list task queries.")
    def put_task_list_queries(self, query_id: int):
        query_name = f'Новый запрос{randint(1,999)}'
        params = f"isClosed=false&isDeleted=false&orderBy=1&searchText=&sortDirection=2"
        start = time.time()
        response = requests.put(
            url=self.endpoints.post_task_list_queries_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.put_task_list_queries_payload(query_id, query_name, params)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully update task list queries.')

    @allure.step("Delete list task queries by list.")
    def delete_task_list_queries_by_list(self, *query_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_task_list_queries_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_task_list_queries_payload(*query_ids)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully delete task list queries by list with IDs: {query_ids}.')

    @allure.step("Delete list task queries by list (remove).")
    def delete_remove_task_list_queries_by_list(self, *query_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_remove_task_list_queries_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_remove_task_list_queries_payload(*query_ids)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully delete task list queries by list with IDs: {query_ids}.')

    @allure.step("Get list task queries by id.")
    def get_task_list_queries_by_id(self, query_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_task_list_queries_by_id_endpoint(query_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, f'Status code {response.status_code}, {response.json()}'
        model = TaskListQueryResultModel(**response.json())
        logger.info(f'Successfully get task list queries with ID: {query_id}.')
        return model

    @allure.step("Delete list task queries by id.")
    def delete_task_list_queries_by_id(self, query_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_task_list_queries_by_id_endpoint(query_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully delete task list queries with ID: {query_id}.')

    @allure.step("Delete list task queries by id (remove).")
    def delete_task_list_queries_by_id_remove(self, query_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_task_list_queries_by_id_endpoint(query_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully delete (remove) task list queries with ID: {query_id}.')
