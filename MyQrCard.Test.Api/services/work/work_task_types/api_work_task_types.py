import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.work.work_task_types.payloads import Payloads
from services.work.work_task_types.endpoints import Endpoints
from config.headers import Headers
from services.work.work_task_types.models.work_task_types_model import *
import time
from http import HTTPStatus
from random import randint
from utils.token_utils import get_token


class WorkTaskTypesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get list task types and returns ID the first existing, check company code.")
    def get_list_task_types_return_first_id(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_task_types_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, f'Status code {response.status_code}, {response.json()}'
        model = SuccessGetListTaskTypesModel(root=response.json())
        for key, value in model.root.items():
            logger.success(f'Successfully get list task types.')
            logger.info(f'Task type ID: {key}, name: {value.name}')
            if "{Company.Code}" in value.numberMask:
                return key, value.name, True
            else:
                return key, value.name, False

    @allure.step("Get list task types.")
    def get_list_task_types(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_task_types_endpoint,
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
            logger.info(f'Tenant does not contain task types.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessGetListTaskTypesModel(root=response.json())
        logger.success(f'Successfully get list a task types.')
        return model

    @allure.step("Update task types.")
    def put_update_task_types(self, task_type_id: int):
        name = f"Тип обновлен авто-тестом {randint(999, 99999)}"
        mask = "[0-9][0-9][0-9][0-9][0-9][0-9][0-9][А-Я][А-Я][А-Я][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]"
        data = {
            "id": task_type_id,
            "name": name,
            "numberMask": mask,
            "closeMinutes": None
        }
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_task_types_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_task_types_payload(data)
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
        model_task_type = self.get_task_type_by_id(task_type_id)
        assert name == model_task_type.name, "Task type is not updated"
        assert mask == model_task_type.numberMask, "Task type is not updated"
        logger.success(f'Successfully update task types ID {task_type_id}.')

    @allure.step("Add task types.")
    def post_add_task_types(self):
        data = {
            "name": f"Тип заявки - {randint(1, 99999)}",
            "numberMask": "[{Now.Day}][{Now.Month}][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]",
            "closeMinutes": None,
            "isDefault": False
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_task_types_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_task_types_payload(data)
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
        model = TaskTypesIdModel(results=response.json())
        logger.success(f'Successfully add task types ID {model.results[0]}.')
        return model

    @allure.step("Delete task types by list.")
    def delete_task_types_by_list(self, *task_type_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_task_types_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_task_types_by_list_payload(*task_type_ids)
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
        logger.success(f'Successfully delete task types ID {task_type_ids}.')

    @allure.step("Get task type by ID.")
    def get_task_type_by_id(self, task_type_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_task_types_by_id_endpoint(task_type_id),
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
        model = GetTaskTypesModel(**response.json())
        logger.success(f'Successfully get task type by ID {task_type_id}.')
        return model

    @allure.step("Delete task types by ID.")
    def delete_task_types_by_id(self, task_type_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_task_types_by_id_endpoint(task_type_id),
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
        logger.success(f'Successfully delete task types ID {task_type_id}.')

    @allure.step("Get list districts task type.")
    def get_list_districts_task_type(self, task_type_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_district_for_task_types_by_id_endpoint(task_type_id),
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
        model = SuccessGetListDistrictsTaskTypesModel(**response.json())
        logger.success(f'Successfully get route a task type.')
        return model

    @allure.step("Get route a task type.")
    def get_route_task_type(self, task_type_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_route_for_task_types_by_id_endpoint(task_type_id),
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
            logger.info("Task type does not contain a route.")
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessGetRouteResultModel(**response.json())
        logger.success(f'Successfully get route a task type.')
        return model

    @allure.step("Get list work types of task types.")
    def get_list_work_types_task_types(self, task_type_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_task_types_related_to_work_types_endpoint(task_type_id),
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
        model = GetListWorkTypesTaskTypes(results=response.json())
        logger.success(f'Successfully list work types of task types.')
        return model

    @allure.step("Add list work types to task type.")
    def post_add_work_types_to_task_types(self, task_type_id: int, *work_types_ids: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_bind_list_work_types_to_task_type_endpoint(task_type_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_work_types_to_task_types_by_list_payload(*work_types_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        logger.success(f'Successfully add list work types {work_types_ids} to task type {task_type_id}.')

    @allure.step("Delete work types from task type by list.")
    def delete_work_types_from_task_type_by_list(self, task_type_id: int, *work_types_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_unbind_work_types_from_task_type_endpoint(task_type_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_unbind_work_types_from_task_type_payload(*work_types_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        logger.success(f'Successfully add list work types {work_types_ids} to task type {task_type_id}.')
