import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.export.tasks.payloads import Payloads
from services.export.tasks.endpoints import Endpoints
from config.headers import Headers
from services.export.tasks.models.export_tasks_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from openpyxl import load_workbook
from io import BytesIO
from urllib import parse


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class ExportTasksAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Returns a list of data available for extended exports.")
    def get_list_data_tasks(self):
        # params = {
        #     "Range": "",
        #     "offset": ""
        # }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_tasks_extended_endpoint,
            headers=self.headers.export_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            f'{response.status_code}, {response.json()}'
        model = SuccessTasksResultModel(list=response.json())
        logger.info(f'Successfully get a list of data available for extended exports.')
        return model

    @allure.step("Exports the task list into account the specified filters by task id.")
    def get_normal_export_task_by_task_id(self, task_id: int, number_task: str, name_task_type: str):
        params = {
            "taskID": task_id,
            "isClosed": False,
            "isDeleted": False,
            "isInitial": False,
            "orderBy": 1
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.export_list_tasks_endpoint, params=params,
            headers=self.headers.export_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.OK, f'{response.status_code}, {response.json()}'
        assert response.headers['Content-Type'] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

        file_stream = BytesIO(response.content)
        workbook = load_workbook(file_stream)

        # СОХРАНЕНИЕ ЛОКАЛЬНО EXCEL
        # output_file_path = "exported_data.xlsx"
        # workbook.save(output_file_path)

        sheet = workbook.active
        sheet_name = workbook.sheetnames

        assert 'Заявки' in sheet_name
        assert sheet['A3'].value == 'Номер', f'Expected Номер, but got {sheet['A3'].value}'
        assert sheet['A4'].value == number_task.strip(), f'Expected {number_task.strip()}, but got {sheet['A4'].value}'
        assert sheet['B3'].value == 'Тип заявки*', f'Expected Тип заявки*, but got {sheet['B3'].value}'
        assert sheet['B4'].value == name_task_type.strip(), f'Expected <{name_task_type.strip()}>, but got {sheet['B4'].value}'
        assert sheet['C3'].value == 'Описание заявки', f'Expected Описание заявки, but got {sheet['C3'].value}'
        assert sheet['C4'].value == 'Заявка создана авто-тестом', f'Expected <Заявка создана авто-тестом>, but got {sheet['C4'].value}'

        logger.warning(parse.unquote(response.headers['Content-Disposition']))
        expected_filename = "Заявки.xlsx"
        expected_content = f'attachment; filename="{expected_filename}"; filename*=UTF-8\'\'"{expected_filename}"'
        decoded_content = parse.unquote(response.headers['Content-Disposition'])
        assert expected_content in decoded_content, f'Expected {expected_content}, but got {decoded_content}'
        logger.info(f'Successfully export of list task by task id.')

    @allure.step("Exports the extended task list taking into account the specified filters by task id.")
    def get_extended_export_task_by_task_id(self, task_id: int, number_task: str):
        start = time.time()
        response = requests.get(
            url=self.endpoints.export_list_extended_tasks_all_filters_by_task_id_endpoint(task_id),
            headers=self.headers.export_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.OK, f'{response.status_code}, {response.json()}'
        assert response.headers['Content-Type'] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

        file_stream = BytesIO(response.content)
        workbook = load_workbook(file_stream)

        # СОХРАНЕНИЕ ЛОКАЛЬНО EXCEL
        # output_file_path = "exported_data.xlsx"
        # workbook.save(output_file_path)

        sheet = workbook.active
        sheet_name = workbook.sheetnames

        assert 'Заявки' in sheet_name
        assert sheet['A2'].value == 'Номер', f'Expected Номер, but got {sheet['A2'].value}'
        assert sheet['A3'].value == number_task.strip(), f'Expected {number_task.strip()}, but got {sheet['A3'].value}'
        assert sheet['B2'].value == 'Тип заявки', f'Expected Тип заявки*, but got {sheet['B2'].value}'
        assert sheet['B3'].value == 'Заявка', f'Expected Заявка, but got {sheet['B3'].value}'
        assert sheet['C2'].value == 'Описание заявки', f'Expected Описание заявки, but got {sheet['C2'].value}'
        assert sheet['C3'].value == 'Заявка создана авто-тестом', f'Expected Заявка создана авто-тестом, but got {sheet['C3'].value}'

        logger.warning(parse.unquote(response.headers['Content-Disposition']))
        expected_filename = "Заявки.xlsx"
        expected_content = f'attachment; filename="{expected_filename}"; filename*=UTF-8\'\'"{expected_filename}"'
        decoded_content = parse.unquote(response.headers['Content-Disposition'])
        assert expected_content in decoded_content, f'Expected {expected_content}, but got {decoded_content}'
        logger.info(f'Successfully export of list task by task id.')
