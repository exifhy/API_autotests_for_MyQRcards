import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.es.districts.payloads import Payloads
from services.es.districts.endpoints import Endpoints
from config.headers import Headers
from services.es.districts.models.districts_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token
from faker import Faker

fake_ru = Faker('ru_RU')


class EsDistrictsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add district.")
    def post_add_district(self):
        district_name = fake_ru.street_title()
        notes_text = 'Участок создан авто-тестом'
        start = time.time()
        response = requests.post(
            url=self.endpoints.add_districts_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.add_districts_payload(
                district_name=district_name,
                notes=notes_text,
                status=False
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
            f'Expected {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessAddDistrictsModel(districts=response.json())
        logger.success(f'Successfully add a non-default district, name district: {district_name}')
        return model

    @allure.step("Add three districts.")
    def post_add_three_districts(self):
        start = time.time()
        response = requests.post(
            url=self.endpoints.add_districts_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.add_districts_args_payload(
                ("Участок-1", f"Описание-1", False),
                ("Участок-2", f"Описание-2", False),
                ("Участок-3", f"Описание-3", False),
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
        model = SuccessAddDistrictsModel(districts=response.json())
        logger.success(f'Successfully add districts with ID: {model.districts}')
        return model

    @allure.step("Marks the district as deleted.")
    def delete_district_by_id(self, district_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_districts_by_id_endpoint(district_id),
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response_headers(response.headers)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.warning(f'Successfully delete district with id: {district_id}.')

    @allure.step('Get detail district info by ID.')
    def get_detail_district_info_by_id(self, district_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_info_district_available_to_user_by_id_endpoint(district_id),
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK,  \
            f'Expected {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessGetInfoDistrictModel(**response.json())
        logger.success(f'Successfully received detail district info with ID {district_id}.')
        return model

    @allure.step("Delete districts by list.")
    def delete_districts_by_list(self, *district_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_districts_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_districts_by_list_payload(*district_id)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, f'{response.status_code}, {response.json()}'
        logger.warning(f'Successfully delete districts with id: {district_id}.')

    @allure.step("Get list districts.")
    def get_list_districts(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_districts_available_to_user_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f"Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}"
        model = SuccessGetListInfoDistrictsModel(result=response.json())
        logger.success(f'Successfully get list districts.')
        return model

    @allure.step("Get list districts with asserts.")
    def get_list_districts_with_asserts(self, district_id: int, deleted: bool):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_districts_available_to_user_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning('No content')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected {HTTPStatus.OK}, but got {response.status_code}. Message {data_response}'
        model = SuccessGetListInfoDistrictsModel(result=response.json())
        for item in model.result:
            if deleted is True:
                if item.id == district_id:
                    raise AssertionError(f'District with ID {district_id} is not deleted.')
            elif deleted is False:
                if item.id == district_id:
                    logger.success(f'Successfully get list districts.')
                    return model

    @allure.step("Update district.")
    def put_update_district(self, district_id):
        district_name = fake_ru.street_title()
        notes_text = 'Участок изменен авто-тестом'
        start = time.time()
        response = requests.put(
            url=self.endpoints.update_districts_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_district_payload(
                district_id=district_id,
                district_name=district_name,
                notes=notes_text,
                status=False
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
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected {HTTPStatus.ACCEPTED}, but got {response.status_code}. Message {data_response}'
        logger.success(f'Successfully update district with ID {district_id}')

    @allure.step("Changes the parent district.")
    def put_update_parent_district(self, district_id, parent_id: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_parent_and_district_sorting_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_parent_district_payload(
                district_id=district_id,
                parent_id=parent_id
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
        assert response.status_code == HTTPStatus.ACCEPTED, f'{response.status_code}, {response.json()}'
        logger.success(f'Successfully changes the parent district.')

    @allure.step("Changes district sorting.")
    def put_update_district_sorting(self, district_id, sorted_order: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_parent_and_district_sorting_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_district_sorting_payload(
                district_id=district_id,
                sorted_id=sorted_order
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
        assert response.status_code == HTTPStatus.ACCEPTED, f'{response.status_code}, {response.json()}'
        logger.success(f'Successfully changes district sorting')
