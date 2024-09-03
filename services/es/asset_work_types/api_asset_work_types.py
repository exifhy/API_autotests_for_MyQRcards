import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.es.asset_work_types.payloads import Payloads
from services.es.asset_work_types.endpoints import Endpoints
from config.headers import Headers
from services.es.asset_work_types.models.asset_work_types_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from faker import Faker

fake_ru = Faker('ru_RU')

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class EsAssetWorkTypesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add work type to asset.")
    def post_add_work_type_to_asset(self, asset_id: int, work_type_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.add_asset_work_type_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.asset_work_types_payload(
                asset_id=asset_id,
                work_type_id=work_type_id,
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
        model = SuccessAssetWorkTypeModel(asset=response.json())
        logger.info(f'Successfully add a non-default work type: {work_type_id} to asset: {asset_id}')
        return model

    @allure.step("Remove from asset work type by ID.")
    def delete_work_type_from_asset_by_id(self, asset_id: int, work_type_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.remove_work_type_from_asset_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.asset_work_types_payload(
                asset_id=asset_id,
                work_type_id=work_type_id,
            )
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}'
        self.attach_time(start, end)
        logger.info(f'Successfully remove from asset: {asset_id} work type by ID: {work_type_id}.')
