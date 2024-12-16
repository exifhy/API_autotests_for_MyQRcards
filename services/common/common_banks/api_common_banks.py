import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.common.common_banks.payloads import Payloads
from services.common.common_banks.endpoints import Endpoints
from config.headers import Headers
from services.common.common_banks.models.common_banks_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
APP_ID = os.getenv('APP_ID')


class CommonBanksAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get list banks.")
    def get_list_banks(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_banks_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
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
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            f'{response.status_code}, {response.json()}'
        model = SuccessGetListBanksModel(root=response.json())
        logger.info(f'Successfully get list banks.')
        return model

    @allure.step("Get list banks and return first bank ID.")
    def get_list_banks_return_first_id(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_banks_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
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
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            f'{response.status_code}, {response.json()}'
        model = SuccessGetListBanksModel(root=response.json())
        logger.info(f'Successfully get list banks.')
        for key, bank in model.root.items():
            logger.info(f"Bank ID: {key}, Name: {bank.name}")
            return int(key)

    @allure.step("Get bank info by ID.")
    def get_info_bank_by_id(self, bank_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_bank_by_id_endpoint(bank_id),
            headers=self.headers.basic_header(API_TOKEN),
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
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            f'{response.status_code}, {response.json()}'
        model = BanksInfoModel(**response.json())
        logger.info(f'Successfully get info bank with ID: {bank_id}.')
        return model
