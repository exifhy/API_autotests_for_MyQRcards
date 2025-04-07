import random
import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.wh.wh_materials.payloads import Payloads
from services.wh.wh_materials.endpoints import Endpoints
from config.headers import Headers
from services.wh.wh_materials.models.wh_materials_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class WhMaterialsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Create materials.")
    def post_add_materials(self):
        number = random.randint(1, 99999)
        name = f"Материал {number}"
        erp_name = f"MErpID {number}"
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_materials_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_materials_payload(
                name,
                currency_id=1,
                unit_id=166,
                erp_name=erp_name
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
        model = SuccessAddMaterialsModel(result=response.json())
        assert response.status_code == HTTPStatus.CREATED, f'{response.status_code}, {response.json()}'
        logger.info(f'Successfully created materials with ID:{model.result[0]}.')
        return model

    @allure.step("Delete materials by list.")
    def delete_materials_by_list(self, *materials_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_materials_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_materials_by_list(*materials_ids)
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
        logger.warning(f'Successfully delete materials with ID:{materials_ids}.')

    @allure.step("Get material by ID.")
    def get_material_by_id(self, materials_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_materials_by_id_endpoint(materials_id),
            headers=self.headers.basic_header(get_token())
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
        assert response.status_code == HTTPStatus.OK, f'{response.status_code}, {response.json()}'
        model = MaterialModel(**response.json())
        logger.warning(f'Successfully get material with Id: {materials_id}.')
        return model
