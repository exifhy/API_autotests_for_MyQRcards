import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.es.asset_types.payloads import Payloads
from services.es.asset_types.endpoints import Endpoints
from config.headers import Headers
from services.es.asset_types.models.es_asset_types_models import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from random import randint


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class EsAssetTypesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add a hostable asset types.")
    def post_add_hostable_asset_types(self):
        name_asset_type = f'Тип объекта: {randint(1, 999)}'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_asset_type_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_add_asset_type_payload(
                name=name_asset_type,
                host=True,
                default=False
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
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, f'{response.status_code}, {response.json()}'
        model = SuccessAddAssetTypesModel(list=response.json())
        logger.info(f'Successfully add a asset type by id: {model.list[0].id}')
        return model

    @allure.step("Update asset types.")
    def put_update_asset_types(self, asset_type_id: int):
        name_asset_type = f'Обновленный тип объекта: {randint(1, 999)}'
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_asset_type_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.put_update_asset_type_payload(
                asset_type_id=asset_type_id,
                name=name_asset_type,
                host=False,
                default=False
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
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, f'{response.status_code}, {response.json()}'
        logger.info(f'Successfully update a asset type by id: {asset_type_id}')
        return name_asset_type

    @allure.step("Delete asset types by ID.")
    def delete_asset_types_by_id(self, asset_type_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_asset_type_by_id_endpoint(asset_type_id),
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
        assert response.status_code == HTTPStatus.ACCEPTED, f'{response.status_code}, {response.json()}'
        logger.info(f'Successfully delete a asset type by id: {asset_type_id}')

    @allure.step("Get list a asset types and return first isHostable=True.")
    def get_list_asset_types_return_is_hostable_true(self):
        """
        Получает список типов оборудования. Ищет первый в списке тип с isHostable=True.
        Если такого нет создает тип оборудования с isHostable=True.
        Возвращает ID тип оборудования первого в списке или созданного типа c isHostable=True.
        """
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_asset_types_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
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
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning(
                'No asset type with isHostable=True not found. Creating a asset type with a isHostable=True.')
            model_hostable = self.post_add_hostable_asset_types()
            return model_hostable.list[0].id
        else:
            assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, (f'{response.status_code}, '
                                                                                         f'{response.json()}')
            model = SuccessGetAssetTypeModel(root=response.json())
            # Поиск первого элемента, где isHostable = True
            for key, asset_type in model.root.items():
                if asset_type.isHostable is True:
                    logger.info(f'Successfully get a list asset type.')
                    logger.warning(f'First asset type with isHostable=True found: {asset_type.name}, Asset Type id: {key}')
                    return int(key)

    @allure.step("Get list asset types.")
    def get_list_asset_types(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_asset_types_endpoint,
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
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, (f'{response.status_code}, '
                                                                                     f'{response.json()}')
        model = SuccessGetAssetTypeModel(root=response.json())
        logger.info(f'Successfully get list a asset type by id: {response.json()}')
        return model

    @allure.step("Geе asset type by ID.")
    def get_asset_type_by_id(self, asset_type_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_asset_type_by_id_endpoint(asset_type_id),
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
        assert response.status_code == HTTPStatus.OK, f'{response.status_code}, {response.json()}'
        model = AssetTypeListResult(**response.json())
        logger.info(f'Successfully get a asset type by id: {asset_type_id}')
        return model
