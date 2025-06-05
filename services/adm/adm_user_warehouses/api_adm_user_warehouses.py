import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.adm.adm_user_warehouses.payloads import Payloads
from services.adm.adm_user_warehouses.endpoints import Endpoints
from config.headers import Headers
from services.adm.adm_user_warehouses.models.adm_user_warehouses_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class AdmUserWarehousesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add warehouses to user.")
    def post_add_warehouses_to_user(self, user_id: int, *warehouses_ids: int or tuple):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_warehouses_to_user_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_warehouses_to_user_payload(user_id, *warehouses_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = UserWarehousesResponseModel(root=response.json())
        logger.info(f'Successfully add user ID {user_id} to warehouses ID {warehouses_ids}.')
        return model

    @allure.step("Delete warehouses from user.")
    def delete_warehouses_from_user(self, user_id: int, *warehouses_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_warehouses_from_user_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_warehouses_from_user_payload(user_id, *warehouses_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.warning(f'Successfully delete user ID {user_id} from warehouses ID {warehouses_ids}.')
        return None
