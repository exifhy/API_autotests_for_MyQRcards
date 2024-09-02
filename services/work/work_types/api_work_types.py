import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.work.work_types.payloads import Payloads
from services.work.work_types.endpoints import Endpoints
from config.headers import Headers
from services.work.work_types.models.work_types_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from faker import Faker

fake_ru = Faker('ru_RU')

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class WorkWorkTypesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add work type.")
    def post_add_work_type(self, param):
        work_type_name = fake_ru.job()
        notes_text = 'Тип работы создан авто-тестом'
        start = time.time()
        response = requests.post(
            url=self.build_url(self.endpoints.add_work_types_endpoint, param),
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.add_work_type_payload(
                work_type_name=work_type_name,
                notes=notes_text,
                status=False
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}'
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        model = SuccessAddWorkTypesModel(type=response.json())
        logger.info(f'Successfully add a non-default work type, name type: {work_type_name}')
        return model

    @allure.step("Marks the work type as remote.")
    def delete_marks_work_type_by_id(self, work_type_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.marks_work_types_as_remote_endpoint(work_type_id),
            headers=self.headers.basic_header(API_TOKEN),
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}'
        self.attach_time(start, end)
        logger.info(f'Successfully marks the work type with id: {work_type_id} as remote.')

    @allure.step("Returns the data for the type of work by id.")
    def get_data_work_type_by_id(self, work_type_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_data_work_types_endpoint(work_type_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, f'Status:{response.status_code}'
        self.attach_time(start, end)
        model = SuccessResultWorkTypeModel(**response.json())
        logger.info(f'Successfully receiving the data work type by id.')
        return model
