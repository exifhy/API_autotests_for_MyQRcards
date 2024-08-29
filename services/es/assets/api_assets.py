import random
import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.es.assets.payloads import Payloads
from services.es.assets.endpoints import Endpoints
from config.headers import Headers
from services.es.assets.models.assets_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from faker import Faker

fake_ru = Faker('ru_RU')

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class EsAssetsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Returns the directory of objects available to the user.")
    def get_directory_of_objects_available_to_user(self, param: dict):
        start = time.time()
        response = requests.get(
            url=self.build_url(self.endpoints.get_directory_of_objects_available_to_user_endpoint, param),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        assert response.status_code == HTTPStatus.PARTIAL_CONTENT, f'Status code {response.status_code}'
        logger.info(response.headers)
        self.attach_response(response.json())
        self.attach_time(start, end)
        model = AssetExtResults(results=response.json())
        logger.info(f'Successfully receiving the assets list.')
        return model

    @allure.step("Object creation.")
    def post_add_object(self):
        name = fake_ru.company()
        notes_text = 'Объект создан авто-тестом'
        start = time.time()
        response = requests.post(
            url=self.endpoints.create_object_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.object_creation_payload(
                parent_id=None,
                name=name,
                company_id=1,
                asset_type_id=2,
                asset_class_is=1,
                notes=notes_text
            )
        )
        end = time.time()
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}'
        logger.info(response.headers)
        self.attach_response(response.json())
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        model = IdNameResultModel(**response.json())
        logger.info(f'Successfully add object without parent object, name object: {name}')
        return model

    @allure.step("Marks the object as remote.")
    def delete_object_by_id(self, asset_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.marks_object_as_remote_endpoint(asset_id),
            headers=self.headers.basic_header(API_TOKEN),
        )
        end = time.time()
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}'
        logger.info(response.headers)
        self.attach_time(start, end)
        logger.info(f'Successfully marks the object with id{asset_id} as remote.')

    @allure.step("Detailed information on the object by id.")
    def get_detailed_information_on_object_by_id(self, asset_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.detailed_information_on_object_endpoint(asset_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        assert response.status_code == HTTPStatus.OK, f'Status code {response.status_code}'
        logger.info(response.headers)
        self.attach_response(response.json())
        self.attach_time(start, end)
        model = AssetDetailedInfoResult(**response.json())
        logger.info(f'Successfully receiving the assets detailed info.')
        return model

    @allure.step("Method of publishing an object.")
    def put_method_of_publishing_an_object_by_id(self, asset_id: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.method_of_publishing_an_object_endpoint(asset_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        assert response.status_code == HTTPStatus.ACCEPTED, f'status code: {response.status_code}'
        self.attach_time(start, end)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(f'Successful publication of the object.')

    @allure.step("Method of publishing an object without bind location.")
    def put_method_of_publishing_an_object_by_id_without_location(self, asset_id: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.method_of_publishing_an_object_endpoint(asset_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        assert response.status_code == HTTPStatus.CONFLICT, f'{response.json()}, status code: {response.status_code}'
        self.attach_time(start, end)
        try:
            self.attach_response(response.json())
            model = ErrorModel(list_model=response.json())
            assert model.list_model[0].code == 'InvalidOperation'
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")

    @allure.step("Update the object by ID.")
    def put_update_object_by_id(self, asset_id: int):
        new_name = f'Изменение имени авто-тестом-{random.randint(1, 999)}'
        new_notes = f'Изменение описания авто-тестом-{random.randint(1, 999)}'
        start = time.time()
        response = requests.put(
            url=self.endpoints.update_object_endpoint(asset_id),
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.object_creation_payload(
                parent_id=None,
                name=new_name,
                company_id=1,
                asset_type_id=2,
                asset_class_is=1,
                notes=new_notes
            )
        )
        end = time.time()
        logger.info(response.headers)
        assert response.status_code == HTTPStatus.ACCEPTED, response.json()
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")

        logger.info(f'Successful update the object, new name object: {new_name}')
