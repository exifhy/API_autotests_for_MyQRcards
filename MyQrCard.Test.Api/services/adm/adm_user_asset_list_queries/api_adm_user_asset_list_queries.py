import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.adm.adm_user_asset_list_queries.payloads import Payloads
from services.adm.adm_user_asset_list_queries.endpoints import Endpoints
from config.headers import Headers
from services.adm.adm_user_asset_list_queries.models.adm_user_asset_list_queries_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class AdmUserAssetListQueriesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add user asset list queries by list.")
    def post_add_user_asset_list_queries_by_list(self, user_id: int, *queries_ids: int or tuple):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_user_asset_list_queries_by_list_endpoint(user_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_user_asset_list_queries_by_list_payload(*queries_ids)
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
        model = UserAssetListQueriesListResponseModel(results=response.json())
        logger.info(f'Successfully add user ID {user_id} asset list queries ID {queries_ids}.')
        return model

    @allure.step("Add user asset list queries.")
    def post_add_user_asset_list_queries(self, user_id: int, *queries_ids: int or tuple):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_user_asset_list_queries_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_user_asset_list_queries_payload(user_id, *queries_ids)
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
        model = UserAssetListQueriesListResponseModel(results=response.json())
        logger.info(f'Successfully add user ID {user_id} asset list queries ID {queries_ids}.')
        return model

    @allure.step("Delete user asset list queries.")
    def delete_user_asset_list_queries(self, user_id: int, *queries_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_user_asset_list_queries_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_user_asset_list_queries_payload(user_id, *queries_ids)
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
        logger.warning(f'Successfully delete user ID {user_id} asset list queries ID {queries_ids}.')
        return None

    @allure.step("Delete user asset list queries by list.")
    def delete_user_asset_list_queries_by_list(self, user_id: int, *queries_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_user_asset_list_queries_by_list_endpoint(user_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_user_asset_list_queries_by_list_payload(*queries_ids)
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
        logger.warning(f'Successfully delete user ID {user_id} asset list queries ID {queries_ids}.')
        return None
