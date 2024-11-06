import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.common.common_attributes.payloads import Payloads
from services.common.common_attributes.endpoints import Endpoints
from config.headers import Headers
from services.common.common_attributes.models.common_attributes_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from random import randint

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
APP_ID = os.getenv('APP_ID')


class CommonAttributesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Attribute creation method for contract only.")
    def post_add_method_attributes_only_for_contract(self):
        """
        Attribute type ID
        1 строка
        2 Целое число
        3
        4
        5
        6 Значение из списка
        7 Множественный выбор из списка
        8 Многострочный текст
        9
        10 Вложенный файл
        """
        attribute_name = f'Доп поле - {randint(1, 999)}'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_method_attributes_endpoint,
            headers=self.headers.auth_header(bearer_token=API_TOKEN, app_id=APP_ID),
            json=self.payloads.post_add_method_attributes_type_str_payloads(
                attribute_name=attribute_name,
                attribute_type_id=1,
                for_task=False,
                for_asset=False,
                for_check_list=False,
                fro_complete_work=False,
                for_contract=True,
                for_company=False
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, f'{response.status_code}, {response.json()}'
        model = SuccessAddAttributeModel(values=response.json())
        logger.warning(f'Successfully attribute creation method only for contract with name: {attribute_name}.')
        return model

    @allure.step("Attribute creation method for asset only type string.")
    def post_add_method_attributes_only_for_asset_str(self):
        attribute_name = f'Доп поле - {randint(1, 999)}'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_method_attributes_endpoint,
            headers=self.headers.auth_header(bearer_token=API_TOKEN, app_id=APP_ID),
            json=self.payloads.post_add_method_attributes_type_str_payloads(
                attribute_name=attribute_name,
                attribute_type_id=1,
                for_task=False,
                for_asset=True,
                for_check_list=False,
                fro_complete_work=False,
                for_contract=False,
                for_company=False
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, f'{response.status_code}, {response.json()}'
        model = SuccessAddAttributeModel(values=response.json())
        logger.warning(f'Successfully attribute type str creation method only for asset with name: {attribute_name}.')
        return model

    @allure.step("Attribute creation method for all relevant essence with type -Value from list-.")
    def post_add_method_attributes_only_for_all_relevant_essence_with_type_6(self):
        """
        Attribute type ID
        6 Значение из списка
        """
        attribute_name = f'Доп поле - {randint(1, 999)}'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_method_attributes_endpoint,
            headers=self.headers.auth_header(bearer_token=API_TOKEN, app_id=APP_ID),
            json=self.payloads.post_add_method_attributes_type_str_payloads(
                attribute_name=attribute_name,
                attribute_type_id=6,
                for_task=True,
                for_asset=True,
                for_check_list=True,
                fro_complete_work=True,
                for_contract=True,
                for_company=True
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, f'{response.status_code}, {response.json()}'
        model = SuccessAddAttributeModel(values=response.json())
        logger.warning(
            f'Successfully attribute creation method for all relevant essence with type '
            f'-Value from list- with name: {attribute_name}.')
        return model

    @allure.step("Attribute deletion method by ID.")
    def delete_method_attribute_by_id(self, attribute_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_method_attribute_by_id_endpoint(attribute_id),
            headers=self.headers.auth_header(bearer_token=API_TOKEN, app_id=APP_ID)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, f'{response.status_code}, {response.json()}'
        logger.warning(f'Successfully delete attribute by ID: {attribute_id}.')

    @allure.step("Get list attributes.")
    def get_list_attributes(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_attributes_endpoint,
            headers=self.headers.auth_header(bearer_token=API_TOKEN, app_id=APP_ID)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            f'{response.status_code}, {response.json()}'
        model = SuccessGetAttributesModel(root=response.json())
        logger.warning(f'Successfully get list attributes.')
        return model

    @allure.step("Get list attributes and return id first attribute for contract.")
    def get_list_attributes_return_id_first_attribute_for_contract(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_attributes_endpoint,
            headers=self.headers.auth_header(bearer_token=API_TOKEN, app_id=APP_ID)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            f'{response.status_code}, {response.json()}'
        model = SuccessGetAttributesModel(root=response.json())
        logger.warning(f'Successfully get list attributes.')
        return model

    @allure.step("Get attribute by ID.")
    def get_attribute_by_id(self, attribute_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_attribute_by_id_endpoint(attribute_id),
            headers=self.headers.auth_header(bearer_token=API_TOKEN, app_id=APP_ID)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            f'{response.status_code}, {response.json()}'
        model = AttributeResultList(**response.json())
        logger.warning(f'Successfully get attribute by ID.')
        return model

    @allure.step("Delete mass attributes.")
    def delete_mass_method_attribute(self, attribute_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_mass_attributes_endpoint,
            headers=self.headers.auth_header(bearer_token=API_TOKEN, app_id=APP_ID),
            json=self.delete_mass_method_attribute(attribute_id)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, f'{response.status_code}, {response.json()}'
        logger.warning(f'Successfully attribute deletion method by ID.')

    @allure.step("Get available values for an attribute.")
    def get_available_values_for_attribute(self, attribute_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_available_values_for_attribute_endpoint(attribute_id),
            headers=self.headers.auth_header(bearer_token=API_TOKEN, app_id=APP_ID)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.error(f'Status code: {response.status_code}, NO CONTENT.')
            return None

        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            f'{response.status_code}, {response.json()}'
        model = SuccessAvailableValuesForAttributeModel(**response.json())
        logger.warning(f'Successfully get available values for an attribute by ID.')
        return model, response.json()
