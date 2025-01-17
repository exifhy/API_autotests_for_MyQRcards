import random
import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.wh.wh_warehouses.payloads import Payloads
from services.wh.wh_warehouses.endpoints import Endpoints
from config.headers import Headers
from services.wh.wh_warehouses.models.wh_warehouses_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class WhWarehousesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Create warehouses.")
    def post_add_warehouses(self):
        """Return model and erp_name in tuple"""
        name = f"Склад-{random.randint(1, 99999)}"
        erp_name = f"Erp {random.randint(1, 99999)}"
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_warehouses_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_add_warehouse_payload(
                name,
                erp_name,
                False
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
        model = SuccessAddWarehousesModel(result=response.json())
        assert response.status_code == HTTPStatus.CREATED, f'{response.status_code}, {response.json()}'
        logger.info(f'Successfully created warehouse with ID:{model.result[0]}.')
        return model, erp_name

    @allure.step("Delete warehouses by list.")
    def delete_warehouses_by_list(self, *wh_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_warehouses_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_warehouses_by_list(*wh_ids)
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
        logger.warning(f'Successfully delete warehouse with ID:{wh_ids}.')

    @allure.step("Get warehouses by ID.")
    def get_warehouses_by_id(self, wh_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_warehouses_by_id_endpoint(wh_id),
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
        model = WarehousesModel(**response.json())
        assert response.status_code == HTTPStatus.OK, f'{response.status_code}, {response.json()}'
        logger.warning(f'Successfully get warehouse with ID: {wh_id}.')
        return model
