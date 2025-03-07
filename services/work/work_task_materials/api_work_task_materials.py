import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.work.work_task_materials.payloads import Payloads
from services.work.work_task_materials.endpoints import Endpoints
from config.headers import Headers
from services.work.work_task_materials.models.work_task_materials_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class WorkTaskMaterialsAPI(Helper):
    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Update task materials.")
    def put_task_materials(self, task_id: int, task_material_id: int, warehouse_id: int):
        data = {
            "id": task_material_id,
            "quantity": 5,
            "warehouseID": warehouse_id
        }
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_task_materials_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.put_task_materials_payload(task_id, data)
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
        logger.info(f'Successfully update task materials.')

    @allure.step("Add task materials.")
    def post_task_materials(self, task_id: int, material_id: int, warehouse_id: int):
        data = {
            "materialID": material_id,
            "takenByUserID": None,
            "quantity": 10,
            "measurementUnitID": 166,
            "warehouseID": warehouse_id
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_task_materials_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_task_materials_payload(task_id, data)
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
        model = SuccessAddTaskMaterialsModel(result=response.json())
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully add task materials.')
        return model

    @allure.step("Delete task materials.")
    def delete_task_materials(self, task_id: int, *material_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_task_materials_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_task_materials_payload(task_id, *material_ids)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}. {data_response}'
        logger.warning(f'Successfully delete task materials with IDs: {material_ids}.')

    @allure.step("Update task materials taken by user On.")
    def put_task_materials_take_on(self, task_id: int, task_material_id: int):
        data = {
            "id": task_material_id,
        }
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_task_materials_take_on_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.put_task_materials_take_on_payload(task_id, data)
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
        logger.info(f'Successfully update task materials taken On.')

    @allure.step("Update task materials taken by user Off.")
    def put_task_materials_take_off(self, task_id: int, *task_material_ids: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_task_materials_take_off_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.put_task_materials_take_off_payload(task_id, *task_material_ids)
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
        logger.info(f'Successfully update task materials taken Off.')
