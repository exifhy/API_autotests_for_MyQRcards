from requests import JSONDecodeError
import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.work.work_checklists.payloads import Payloads
from services.work.work_checklists.endpoints import Endpoints
from config.headers import Headers
from services.work.work_checklists.models.work_checklists_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from random import randint

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class WorkChecklistsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add checklists.")
    def post_add_checklists(self):
        name = f'Чек-лист-{randint(1, 999)}'
        description = f'Описание-{randint(1, 999)}'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_checklists_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_add_checklists_payload(
                name=name,
                desc=description
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}, {response.json()}'
        model = SuccessAddChecklistsToAssetModel(result=response.json())
        logger.info(f'Successfully add checklists with name {name}.')
        return model

    @allure.step("Delete checklist by ID.")
    def delete_checklist_by_id(self, checklist_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_checklist_by_id_endpoint(checklist_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.warning(f'Successfully delete checklist with ID: {checklist_id}.')

    @allure.step("Get checklist by ID.")
    def get_checklist_by_id(self, checklist_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_checklist_by_id_endpoint(checklist_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, f'Status code {response.status_code}, {response.json()}'
        model = SuccessGetChecklistByIdResultModel(**response.json())
        logger.warning(f'Successfully get checklist by ID: {checklist_id}.')
        return model

    @allure.step("Delete checklist by list.")
    def delete_checklist_by_list(self, *args):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_checklists_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_checklists_payloads(*args)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.warning(f'Successfully delete checklists with ID: {args}.')

    @allure.step("Get list checklists.")
    def get_list_checklists(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_active_checklists_endpoint,
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info(f'NO CONTENT: status code 204.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetListChecklistsModel(root=response.json())
        logger.warning(f'Successfully get checklists by list.')
        return model

    @allure.step("Update checklists.")
    def put_update_checklists(self, checklist_id: int):
        name = f'Измененный-чек-лист-{randint(1, 999)}'
        description = f'Чек лист изменен-{randint(1, 999)}'
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_checklists_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.put_update_checklists_payload(
                checklist_id=checklist_id,
                name=name,
                desc=description
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully update checklists with ID: {checklist_id}.')

    @allure.step("Assign checklist identifiers in the tables of assets and work types.")
    def post_checklists_assign(self, checklist_id: int, asset_id: int, work_type_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_checklist_identifiers_in_tables_of_asset_and_work_types_endpoint(checklist_id),
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_checklists_assign_payload(
                asset_id,
                work_type_id=work_type_id
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.info(
            f'Successfully assign checklist ID:{checklist_id} to assets ID:{asset_id} and work types ID:{work_type_id}.'
        )

    @allure.step("Delete assign checklist identifiers in the tables from assets and work types.")
    def delete_checklists_assign(self, checklist_id: int, asset_id: int, work_type_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_checklist_identifiers_from_tables_of_asset_and_work_types_endpoint(checklist_id),
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_checklists_assign_payload(
                asset_id,
                work_type_id=work_type_id
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.warning(
            f'Successfully delete assign checklist ID:{checklist_id} to assets ID:{asset_id} '
            f'and work types ID:{work_type_id}.'
        )

    @allure.step("Get checklist items by ID.")
    def get_checklist_items_by_id(self, checklist_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_items_checklist_endpoint(checklist_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, f'Status code {response.status_code}, {response.json()}'
        model = SuccessGetListChecklistsItemsModel(root=response.json())
        logger.info(f'Successfully get checklist items with ID: {checklist_id}.')
        return model
