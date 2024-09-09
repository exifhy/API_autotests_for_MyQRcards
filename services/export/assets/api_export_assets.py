from urllib import parse
import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.export.assets.payloads import Payloads
from services.export.assets.endpoints import Endpoints
from config.headers import Headers
from services.export.assets.models.export_assets_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from faker import Faker
from openpyxl import load_workbook
from io import BytesIO


fake_ru = Faker('ru_RU')

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class ExportAssetsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Returns a list of data available for advanced exports.")
    def get_list_of_data_available_for_advanced_exports(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.export_list_object_extended_includes_endpoint,
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, f'Status code {response.status_code}'
        self.attach_time(start, end)
        model = SuccessExportDataListModel(result=response.json())
        logger.info(f'Successfully receiving the list of data available for advanced exports.')
        return model

    @allure.step("Normal export a list of objects.")
    def get_normal_export_list_objects(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.normal_export_list_object_endpoint,
            headers=self.headers.export_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_time(start, end)
        try:
            logger.warning(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.OK, f'Status code {response.status_code}'
        assert response.headers['Content-Type'] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

        file_stream = BytesIO(response.content)
        workbook = load_workbook(file_stream)

        # СОХРАНЕНИЕ ЛОКАЛЬНО EXCEL
        # output_file_path = "exported_data.xlsx"
        # workbook.save(output_file_path)

        sheet = workbook.active
        sheet_name = workbook.sheetnames

        # ВЫВОД СТРОК EXCEL ФАЙЛА
        # count = 0
        # for row in sheet.iter_rows(values_only=True):
        #     logger.warning(row)
        #     count += 1
        #     if count >= 10:
        #         break

        assert 'Объекты и оборудование' in sheet_name
        assert sheet['A3'].value == 'Название*'
        assert sheet['B3'].value == 'ERP ID'
        assert sheet['C3'].value == 'Компания*'
        assert sheet['D3'].value == 'Тип*'
        assert sheet['E3'].value == 'Класс*'
        assert sheet['F3'].value == 'Участок*'
        assert sheet['G3'].value == 'Вид работ*'
        assert sheet['I3'].value == 'Адрес*'

        logger.warning(parse.unquote(response.headers['Content-Disposition']))
        expected_filename = "Объекты+и+оборудование.xlsx"
        expected_content = f'attachment; filename="{expected_filename}"; filename*=UTF-8\'\'"{expected_filename}"'
        decoded_content = parse.unquote(response.headers['Content-Disposition'])
        assert expected_content in decoded_content, f'Expected {expected_content}, but got {decoded_content}'
        logger.info(f'Successfully receiving the normal export of list object.')

    @allure.step("Exports a list of objects with a set of filters by assetID(filter set in test case 23132).")
    def get_export_list_with_set_filter_by_asset_id(self, name_asset: str, asset_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.export_all_filters_by_asset_id_endpoint(asset_id),
            headers=self.headers.export_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        # logger.warning(response.request.url)
        self.attach_time(start, end)
        try:
            self.attach_response(response.json())
            logger.warning(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")

        assert response.status_code == HTTPStatus.OK, f'Status code {response.status_code}'
        assert response.headers['Content-Type'] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

        file_stream = BytesIO(response.content)
        workbook = load_workbook(file_stream)

        # output_file_path = "exported_data.xlsx"
        # workbook.save(output_file_path)

        sheet = workbook.active
        sheet_name = workbook.sheetnames

        # count = 0
        # for row in sheet.iter_rows(values_only=True):
        #     logger.warning(row)
        #     count += 1
        #     if count >= 5:
        #         break

        # logger.info(sheet_name)
        assert 'Объекты и оборудование' in sheet_name
        assert sheet['A3'].value == 'Название'
        assert sheet['A4'].value == name_asset
        assert sheet['B3'].value == 'Компания'
        assert sheet['B4'].value == 'Первая компания'
        assert sheet['C3'].value == 'Тип объекта'
        assert sheet['C4'].value == 'Объект'
        assert sheet['D3'].value == 'Класс объекта'
        assert sheet['D4'].value == 'По умолчанию'
        assert sheet['E3'].value == 'Участок'
        assert sheet['E4'].value == 'Основной'
        assert sheet['F3'].value == 'Вид работ'
        assert sheet['F4'].value == 'Ремонт'

        logger.warning(parse.unquote(response.headers['Content-Disposition']))
        expected_filename = "Объекты+и+оборудование.xlsx"
        expected_content = f'attachment; filename="{expected_filename}"; filename*=UTF-8\'\'"{expected_filename}"'
        decoded_content = parse.unquote(response.headers['Content-Disposition'])
        assert expected_content in decoded_content, f'Expected {expected_content}, but got {decoded_content}'
        logger.info(f'Successfully receiving the xlsx with set filter by assetID.')
