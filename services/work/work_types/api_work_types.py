import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.work.work_types.payloads import Payloads
from services.work.work_types.endpoints import Endpoints
from config.headers import Headers
from services.work.work_types.models.work_types_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from faker import Faker

fake_ru = Faker('ru_RU')

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class WorkWorkTypesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add work type.")
    def post_add_work_type(self, param):
        work_type_name = fake_ru.job()
        notes_text = 'Тип работы создан авто-тестом'
        start = time.time()
        response = requests.post(
            url=self.endpoints.add_work_types_endpoint, params=param,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.add_work_type_payload(
                work_type_name=work_type_name,
                notes=notes_text,
                status=False
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
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}, {response.json()}'
        model = SuccessAddWorkTypesModel(type=response.json())
        logger.info(f'Successfully add a non-default work type, name type: {work_type_name}')
        return model

    @allure.step("Delete the work type.")
    def delete_marks_work_type_by_id(self, work_type_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_work_types_endpoint(work_type_id),
            headers=self.headers.basic_header(API_TOKEN),
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully delete the work type with id: {work_type_id}.')

    @allure.step("Returns the data for the type of work by id.")
    def get_data_work_type_by_id(self, work_type_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_data_work_types_endpoint(work_type_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            f'Status:{response.status_code}, {response.json()}'
        model = SuccessResultWorkTypeModel(**response.json())
        logger.info(f'Successfully receiving the data work type by id.')
        return model

    @allure.step("Get list a type of work.")
    def get_list_work_type(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_work_types_endpoint,
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
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, (f'{response.status_code}, '
                                                                                     f'{response.json()}')
        model = SuccessGetWorkTypesModel(root=response.json())
        logger.info(f'Successfully get list a work type.')
        return model

    @allure.step("Get list a type of work from asset by ID and return name work types.")
    def get_list_work_type_from_asset_by_id(self, asset_id: int):
        """Get list a type of work from asset by ID and return name work types."""
        params = {
            "isPublished": True,
            "assetID": asset_id
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_work_types_endpoint, params=params,
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
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, (f'{response.status_code}, '
                                                                                     f'{response.json()}')
        model = SuccessGetWorkTypesModel(root=response.json())
        logger.info(f'Successfully get list a work type from asset by iD: {asset_id}.')
        if model.root:
            int_keys_root = {int(key): value for key, value in model.root.items()}
            min_key = min(int_keys_root.keys())
            name = int_keys_root[min_key].name
            logger.info(f'Smallest ID: {min_key} with name: {name}')
            return name

    @allure.step("Get list a type of work and return ID first published type.")
    def get_list_work_type_return_id_first_published_type(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_work_types_endpoint,
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
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning('Published type not found. Creating a published work type.')
            model_work_type = self.post_add_work_type({"relatedToAnyTaskType": "true"})
            self.put_publish_complete_work_types(model_work_type.type[0])
            return model_work_type.type[0]
        else:
            assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, (f'{response.status_code}, '
                                                                                         f'{response.json()}')
            model = SuccessGetWorkTypesModel(root=response.json())
            for key, value in model.root.items():
                if value.published is not None:
                    logger.info(f'Successfully get list a work type.')
                    logger.warning(f'First published work type found: {value.name}, Work Type id: {key}')
                    return int(key)

    @allure.step("Publishes completed works.")
    def put_publish_complete_work_types(self, work_type_id: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_work_types_publish_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.publish_work_types_payload(
                work_type_id=work_type_id
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
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully publish work type, id type: {work_type_id}')

    @allure.step("Publishes completed works by id.")
    def put_publish_complete_work_types_by_id(self, work_type_id: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_work_types_publish_by_id_endpoint(worktype_id=work_type_id),
            headers=self.headers.basic_header(API_TOKEN),
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully publish work type by id, type id: {work_type_id}')

    @allure.step("Cancels publication of completed work by id.")
    def put_unpublish_complete_work_types_by_id(self, work_type_id: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_work_types_unpublish_by_id_endpoint(worktype_id=work_type_id),
            headers=self.headers.basic_header(API_TOKEN),
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully unpublish work type by id, type id: {work_type_id}')

    @allure.step("Cancels publication of completed work.")
    def put_unpublish_complete_work_types(self, work_type_id: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_work_types_unpublish_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.unpublish_work_types_payload(work_type_id=work_type_id)
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
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully unpublish work type, type id: {work_type_id}')
