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

    @allure.step("Add asset types.")
    def post_add_asset_types(self, host: bool):
        name_asset_type = f'Тип объекта: {randint(1, 999)}'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_asset_type_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_add_asset_type_payload(
                name=name_asset_type,
                host=host,
                default=False
            )
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessAddAssetTypesModel(list=response.json())
        logger.info(f'Successfully add a asset type by id: {model.list[0].id}')
        return model

    @allure.step("Update asset types.")
    def put_update_asset_types(self, asset_type_id: int, host: bool):
        name_asset_type = f'Обновленный тип объекта: {randint(1, 999)}'
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_asset_type_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.put_update_asset_type_payload(
                asset_type_id=asset_type_id,
                name=name_asset_type,
                host=host,
                default=False
            )
        )
        end = time.time()
        data_response = self.response_content(response)
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.info(f'Successfully update a asset type with id: {asset_type_id}')
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
        logger.warning(f'Successfully delete a asset type by id: {asset_type_id}')

    @allure.step("Delete asset types by list.")
    def delete_asset_types_by_list(self, *asset_type_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_asset_types_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_asset_types_by_list_payload(*asset_type_ids)
        )
        end = time.time()
        data_response = self.response_content(response)
        logger.info(response.headers)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected {response.status_code}, {response.json()}'
        logger.warning(f'Successfully delete a asset types by list id: {asset_type_ids}')

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
            model_hostable = self.post_add_asset_types(True)
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
    def get_list_asset_types(self, *asset_type_ids: int or None):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_asset_types_endpoint,
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        data_response = self.response_content(response)
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessGetAssetTypeModel(root=response.json())
        if asset_type_ids is not None:
            for item in asset_type_ids:
                assert str(item) in model.root, \
                    f'Asset type with ID {item} is not in the list asset types'
        logger.info(f'Successfully get list a asset types.')
        return model

    @allure.step("Get all list asset types.")
    def get_all_list_asset_types(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_asset_types_endpoint,
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        data_response = self.response_content(response)
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning("Asset types not found")
            return None
        else:
            assert response.status_code == HTTPStatus.OK, \
                f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
            model = SuccessGetAssetTypeModel(root=response.json())
            logger.info(f'Successfully get list a asset types.')
            return model

    @allure.step("Get list asset types check data.")
    def get_list_asset_types_check_data_by_id(self, name: str, *asset_type_ids: int or None):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_asset_types_endpoint,
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        data_response = self.response_content(response)
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessGetAssetTypeModel(root=response.json())
        if asset_type_ids is not None:
            for item in asset_type_ids:
                assert str(item) in model.root, \
                    f'Asset type with ID {item} is not in the list asset types'
                assert model.root[str(item)].name == name, \
                    f'Asset type with ID {item} is not update'
        logger.info(f'Successfully get list a asset types.')
        return model

    @allure.step("Get list asset types, check asset type is deleted.")
    def get_list_asset_types_is_deleted(self, *asset_type_ids: int or None):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_asset_types_endpoint,
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        data_response = self.response_content(response)
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessGetAssetTypeModel(root=response.json())
        if asset_type_ids is not None:
            for item in asset_type_ids:
                assert str(item) not in model.root, \
                    f'Asset type with ID {item} is not deleted.'
        logger.info(f'Successfully get list a asset types.')
        return model

    @allure.step("Get asset type by ID.")
    def get_asset_type_by_id(self, asset_type_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_asset_type_by_id_endpoint(asset_type_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        data_response = self.response_content(response)
        logger.info(response.headers)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = AssetTypeListResult(**response.json())
        logger.info(f'Successfully get a asset type by id: {asset_type_id}')
        return model

    @allure.step("Get deleted asset type by ID.")
    def get_deleted_asset_type_by_id(self, asset_type_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_asset_type_by_id_endpoint(asset_type_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        data_response = self.response_content(response)
        logger.info(response.headers)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.NO_CONTENT, \
            f'Expected status code {HTTPStatus.NO_CONTENT}, but got {response.status_code}, {data_response}'
        logger.info(f'Successfully get deleted a asset type with ID: {asset_type_id}')
