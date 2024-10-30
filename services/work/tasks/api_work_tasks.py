import random
import allure
import requests
from datetime import timezone
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.work.tasks.payloads import Payloads
from services.work.tasks.endpoints import Endpoints
from config.headers import Headers
from services.work.tasks.models.work_tasks_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class WorkTasksAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add task.")
    def post_add_task(self, asset_id: int, company_id: int, work_type_id: str, criticality_id: str, task_type_id: str):
        additional_data = {
            "AssetID": asset_id,
            "WorkTypeID": work_type_id,
            "companyID": company_id
        }
        date = datetime.now(timezone.utc).isoformat(timespec='milliseconds')
        current_time_iso = date.replace('+00:00', 'Z')
        task_number = str(random.randint(999, 99999))
        note_task = f'Заявка создана авто-тестом'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_task_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.add_task_payload(
                criticality_id=criticality_id,
                task_type_id=task_type_id,
                number=task_number,
                note=note_task,
                date=current_time_iso,
                **additional_data
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}, {response.json()}'
        model = SuccessAddTasksModel(**response.json())
        logger.info(f'Successfully add a task, number task: {task_number}')
        return model

    @allure.step("Delete the task.")
    def delete_task_by_id(self, task_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_task_by_id_endpoint(task_id),
            headers=self.headers.basic_header(API_TOKEN),
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        model = SuccessDeleteTaskModel(list=response.json())
        logger.info(f'Successfully delete the task with id: {model.list[0].taskID}.')
        return model

    @allure.step("Returns a list of tasks available to the user.")
    def get_list_of_tasks_available_to_user(self):
        params = {
            "fetch": 100,
            "isClosed": False,
            "isDeleted": False,
            "offset": 0,
            "orderBy": 1,
            "sortDirection": 2,
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_task_endpoint, params=params,
            headers=self.headers.basic_header(API_TOKEN),
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
        model = SuccessTaskListResultModel(**response.json())
        logger.info(f'Successfully returns a list of tasks available to the user.')
        return model

    @allure.step("Returns detailed information on the task by id.")
    def get_detailed_info_task_by_id(self, task_id: int):
        # params = {
        #     "taskSnapshotID": int,
        #     "includeSchedule": bool
        # }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_detailed_info_task_by_id_endpoint(task_id),
            headers=self.headers.basic_header(API_TOKEN),
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, f'Status code {response.status_code}, {response.json()}'
        model = SuccessDetailedInfoModel(**response.json())
        logger.info(f'Successfully returns detailed information on the task by id.')
        return model

    @allure.step("Update task by id.")
    def put_update_task_by_id(self, task_id: int):
        date = datetime.now(timezone.utc).isoformat(timespec='milliseconds')
        current_time_iso = date.replace('+00:00', 'Z')
        task_number = str(random.randint(999, 99999))
        note_task = 'Заявка изменена авто-тестом'
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_task_by_id_endpoint(task_id),
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.put_update_task_payload(
                number=task_number,
                note=note_task,
                date=current_time_iso
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully update information on the task by id.')
        return task_number, note_task

    @allure.step("Returns the list of available stages to which the task can be transferred.")
    def get_list_of_available_stages_to_task_can_transferred(self, task_id: int, stage_name: str, token: str) -> str:
        # params = {
        #     "Range": "items=0-10",
        #     "offset": '10',
        #     "fetch": '50',
        # }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_of_available_stages_to_task_can_transferred_endpoint(task_id),
            headers=self.headers.basic_header(token),
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
        model = SuccessGetListStagesModel(root=response.json())
        for key, value in model.root.items():
            if value.name == stage_name:
                logger.info(f'Successfully get the list of available stages to which the task can be transferred.')
                logger.info(f"Stage ID: {key}, Name: {value.name}")
                return key
