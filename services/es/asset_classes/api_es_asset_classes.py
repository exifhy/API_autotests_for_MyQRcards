import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.es.asset_classes.payloads import Payloads
from services.es.asset_classes.endpoints import Endpoints
from config.headers import Headers
from services.es.asset_classes.models.es_asset_classes_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from random import randint


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class EsAssetClassesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add asset class.")
    def post_add_asset_class(self):
        name_asset_class = f'Класс оборудования: {randint(1, 9999)}'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_asset_class_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_add_asset_class_payload(
                name=name_asset_class,
                default=False
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, f'{response.status_code}, {response.json()}'
        model = SuccessAddAssetClassesModel(list=response.json())
        logger.info(f'Successfully add a asset class by id: {model.list[0].id}')
        return model, name_asset_class

    @allure.step("Get list a asset classes and return ID first class.")
    def get_list_asset_classes_return_id_first_class(self):
        """
        Получает список классов объектов. Ищет первый в списке класс.
        Если нет создает новый.
        Возвращает первый в списке ID класса объекта или созданного класса.
        """
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_asset_classes_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
            self.attach_response_headers(response.headers)
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning('No asset class found. Creating a asset class.')
            model_asset_class = self.post_add_asset_class()
            return model_asset_class[0].list[0].id
        else:
            assert response.status_code == HTTPStatus.OK, f'{response.status_code}, {response.json()}'
            model = SuccessGetAssetClassesModel(root=response.json())
            for key, asset_class in model.root.items():
                logger.info(f'Successfully get a list asset classes.')
                logger.info(f"Class ID: {key}, Name: {asset_class.name}")
                return int(key)

    @allure.step("Get list a asset classes.")
    def get_list_asset_classes(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_asset_classes_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        model = SuccessGetAssetClassesModel(root=response.json())
        logger.info(f'Successfully get list a asset class.')
        return model

    @allure.step("Update asset class.")
    def put_update_asset_class(self, asset_class_id: int):
        name_asset_class = f'Обновленный класс: {randint(1, 9999)}'
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_asset_class_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.put_update_asset_class_payload(
                asset_class_id=asset_class_id,
                name=name_asset_class,
                default=False
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, f'{response.status_code}, {response.json()}'
        logger.info(f'Successfully update a asset class by id.')

    @allure.step("Delete mass asset classes.")
    def delete_mass_asset_classes(self, *args):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_asset_class_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_asset_class_payload(
                *args
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, f'{response.status_code}, {response.json()}'
        logger.info(f'Successfully delete asset class mass.')

    @allure.step("Delete asset classes by ID.")
    def delete_asset_classes_by_id(self, asset_class_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_asset_class_by_id_endpoint(asset_class_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, f'{response.status_code}, {response.json()}'
        logger.info(f'Successfully delete asset class by ID.')

    @allure.step("Get asset classes by ID.")
    def get_asset_classes_by_id(self, asset_class_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_asset_class_by_id_endpoint(asset_class_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, f'{response.status_code}, {response.json()}'
        model = AssetClassesResult(**response.json())
        logger.info(f'Successfully get asset class by ID.')
        return model
