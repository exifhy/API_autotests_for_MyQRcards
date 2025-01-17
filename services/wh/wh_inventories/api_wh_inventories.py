import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.wh.wh_inventories.payloads import Payloads
from services.wh.wh_inventories.endpoints import Endpoints
from config.headers import Headers
from services.wh.wh_inventories.models.wh_inventories_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from datetime import datetime


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


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
            "Quantity": 100.0,
            "MeasurementUnitID": 166,
            "MaterialCurrencyID": 1,
            "MaterialCost": 1.0,
            "WarehouseErpID": wh_erp,
            "WarehouseName": wh_name
        }
        current_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_inventories_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_add_inventories_payload(
                current_date,
                data
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
        model = SuccessAddInventoriesModel(result=response.json())
        assert response.status_code == HTTPStatus.CREATED, f'{response.status_code}, {response.json()}'
        logger.info(f'Successfully created inventory with ID:{model.result[0].id}.')
        return model
