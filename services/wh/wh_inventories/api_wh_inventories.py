import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.wh.wh_inventories.payloads import Payloads
from services.wh.wh_inventories.endpoints import Endpoints
from config.headers import Headers
from services.wh.wh_inventories.models.wh_inventories_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token
from datetime import datetime, timedelta


class WhInventoriesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Create inventories.")
    def post_add_inventories(self, material_erp: str, material_name: str, wh_erp: str, wh_name: str):
        """Quantity 100, kilogram, ruble, cost 1"""
        data = {
            "MaterialErpID": material_erp,
            "MaterialName": material_name,
            "Quantity": 1000.0,
            "MeasurementUnitID": 166,
            "MaterialCurrencyID": 1,
            "MaterialCost": 500.0,
            "WarehouseErpID": wh_erp,
            "WarehouseName": wh_name
        }
        current_date = datetime.now() - timedelta(minutes=180)
        formatted_date = current_date.strftime("%Y-%m-%dT%H:%M:%S")
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_inventories_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_inventories_payload(
                formatted_date,
                data
            )
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response_headers(response.headers)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessAddInventoriesModel(result=response.json())
        logger.info(f'Successfully created inventory with ID:{model.result[0].id}.')
        return model

    @allure.step("Delete inventories by list.")
    def delete_inventories_by_list(self, *inventory_ids: str):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_inventories_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_inventories_by_list_payload(
                *inventory_ids
            )
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.warning(f'Successfully delete inventory with IDs: {inventory_ids}.')
        return None
