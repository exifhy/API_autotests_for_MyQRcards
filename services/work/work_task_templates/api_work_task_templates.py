import random
from datetime import datetime
import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.work.work_task_templates.payloads import Payloads
from services.work.work_task_templates.endpoints import Endpoints
from config.headers import Headers
from services.work.work_task_templates.models.work_task_templates_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class WorkTaskTemplatesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add task templates.")
    def post_add_task_templates(self, asset_id: int):
        name = f"Шаблон заявки - {random.randint(1, 999)}"
        note = "Создана авто-тестом"
        start = time.time()
        response = requests.post(
            url=self.endpoints.add_task_templates_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.add_task_templates_payloads(
                template_name=name,
                templates_note=note,
                asset_id=asset_id,
                task_type_id="7",
                work_type_id="3"
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_request(response.request.body)
        self.attach_time(start, end)
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}'
        model = SuccessAddTaskTemplatesModel(templates=response.json())
        logger.info(f'Successfully created task templates with id: {model.templates[0]} ')
        return model

    @allure.step("Returns a list of task templates by ID.")
    def get_list_task_templates_by_id(self, task_templates_id: str):
        params = {
            "taskTemplateID": task_templates_id
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_task_templates_endpoint, params=params,
            headers=self.headers.basic_header(API_TOKEN),
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, f'Status code {response.status_code}'
        model = SuccessGetTaskTemplatesModel(**response.json())
        logger.info(f'Successfully received list task templates with id: {model.root[task_templates_id].id}')
        logger.info(f'Successfully received list task templates with name: {model.root[task_templates_id].name}')
        logger.info(f'Successfully received list task templates with notes: {model.root[task_templates_id].notes}')
        return model

    @allure.step("Delete task templates by ID.")
    def delete_task_templates_by_id(self, task_templates_id: str):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_task_templates_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_task_templates_payloads(task_templates_id)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_request(response.request.body)
        self.attach_time(start, end)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}'
        logger.info(f'Successfully delete task templates by ID')

    @allure.step("Binds employee to the template by ID.")
    def post_bind_employee_to_template_by_id(self, task_templates_id: str, user_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.assignment_task_templates_endpoint(task_templates_id),
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.bind_employee_to_template_payloads(user_id)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_request(response.request.body)
        self.attach_time(start, end)
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}'
        model = SuccessTaskTemplateAssignmentMergeModel(task=response.json())
        logger.info(f'Successfully binds employee to the template by ID.')
        return model

    @allure.step("Add template requests for the schedule by ID.")
    def post_add_task_templates_for_schedules_by_id(self, task_templates_id: str, schedule_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.task_templates_for_schedules_endpoint(task_templates_id),
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.add_task_templates_for_schedules_payloads(schedule_id)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_request(response.request.body)
        self.attach_time(start, end)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}'
        logger.info(f'Successfully add template requests for the schedule by ID.')

    @allure.step("Schedule activation by ID.")
    def put_schedule_activation_by_id(self, task_templates_id: str, schedule_id: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.activate_schedule_endpoint(task_templates_id, schedule_id),
            headers=self.headers.basic_header(API_TOKEN),
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}'
        model = SuccessActivateTaskTemplatesSchedulesModel(**response.json())
        assert model.isActive is True, f'Expected True, but got {model.isActive}'
        logger.info(f'Successfully schedule activation by ID.')
        return model

    @allure.step("Schedule deactivation by ID.")
    def put_schedule_deactivation_by_id(self, task_templates_id: str, schedule_id: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.deactivate_schedule_endpoint(task_templates_id, schedule_id),
            headers=self.headers.basic_header(API_TOKEN),
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}'
        logger.info(f'Successfully schedule deactivation by ID.')

