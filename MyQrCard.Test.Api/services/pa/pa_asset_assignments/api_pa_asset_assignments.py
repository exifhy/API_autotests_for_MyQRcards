import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.pa.pa_asset_assignments.payloads import Payloads
from services.pa.pa_asset_assignments.endpoints import Endpoints
from config.headers import Headers
from services.pa.pa_asset_assignments.models.pa_asset_assignments_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class PaAssetAssignmentsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get list asset assignments by user ID.")
    def get_list_asset_assignments_by_user_id(self, user_id: int):
        params = {
            "userID": user_id
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_asset_assignments_endpoint, params=params,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list asset assignments.")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}, {data_response}')
        model = AssetAssignmentsListResponse(results=response.json())
        logger.info(f'Successfully get list asset assignments by user ID {user_id}.')
        return model

    @allure.step("Add asset assignments to user.")
    def post_add_asset_assignments(self, user_id: int, asset_id: int):
        data = {
            "assetID": asset_id,
            "userID": user_id,
            "dateFrom": datetime.now().strftime('%Y-%m-%d'),
            "notes": "Авто тест",
            "dateTill": "9999-01-01"
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_asset_assignments_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_asset_assignments_payload(data)
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
            (f'Expected status code {HTTPStatus.CREATED}, '
             f'but got {response.status_code}, {data_response}')
        logger.info(f'Successfully add asset assignments to user ID {user_id}.')
        return None

    @allure.step("Delete asset assignments.")
    def delete_asset_assignments(self, user_id: int, asset_id: int):
        data = {
            "assetID": asset_id,
            "userID": user_id,
            "dateTill": "9999-01-01"
        }
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_asset_assignments_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_users_asset_assignments_payload(data)
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
            (f'Expected status code {HTTPStatus.ACCEPTED}, '
             f'but got {response.status_code}, {data_response}')
        logger.warning(f"Successfully delete asset assignments {user_id}.")
        return None
