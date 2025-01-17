import random

import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.wh.wh_receipts.payloads import Payloads
from services.wh.wh_receipts.endpoints import Endpoints
from config.headers import Headers
from services.wh.wh_receipts.models.wh_receipts_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class WhReceiptsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add receipts.")
    def post_add_receipts(self, wh_id: int, erp_name: str):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_receipts_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_add_receipt_payload(wh_id, 2, erp_name)
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
        model = SuccessAddReceiptsModel(result=response.json())
        assert response.status_code == HTTPStatus.CREATED, f'{response.status_code}, {response.json()}'
        logger.info(f'Successfully created receipt with ID:{model.result[0]}.')
        return model

    @allure.step("Add items receipts.")
    def post_add_items_receipts(self, receipt_id: int, material_id: int):
        qty = random.randint(1, 999)
        unit_id = 166
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_items_receipts_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_add_items_receipt_payload(
                receipt_id,
                material_id,
                unit_id,
                qty
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
        assert response.status_code == HTTPStatus.ACCEPTED, f'{response.status_code}, {response.json()}'
        logger.info(f'Successfully add items to receipt with ID:{material_id}.')

    @allure.step("Delete receipts by list.")
    def delete_receipts_by_list(self, *receipt_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_receipts_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_receipts_payload(
                *receipt_ids
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
        assert response.status_code == HTTPStatus.ACCEPTED, f'{response.status_code}, {response.json()}'
        logger.warning(f'Successfully delete receipts with ID:{receipt_ids}.')

    @allure.step("Delete items receipts by list.")
    def delete_items_receipts_by_list(self, receipt_id: int, *items_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_items_receipts_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_items_receipts_payload(
                receipt_id,
                *items_ids
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
        assert response.status_code == HTTPStatus.ACCEPTED, f'{response.status_code}, {response.json()}'
        logger.warning(f'Successfully delete items receipts with ID:{items_ids}.')
