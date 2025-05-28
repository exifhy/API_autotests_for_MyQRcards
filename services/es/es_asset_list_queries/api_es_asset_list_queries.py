import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.es.es_asset_list_queries.payloads import Payloads
from services.es.es_asset_list_queries.endpoints import Endpoints
from config.headers import Headers
from services.es.es_asset_list_queries.models.es_asset_list_queries_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token
from random import randint


class EsAssetListQueriesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add queries and binds it to the current user.")
    def post_add_queries_binds_to_user(
            self,
            token,
            company_id,
            work_type_id,
            asset_type_id,
            asset_class_id,
            district_id,
            tenant_id
    ):
        name_query = f"Запрос {randint(1, 99)}"
        value_query = (f"companyID={company_id}&workTypeID={work_type_id}&warrantyTill=9999-12-31T23%3A59%3A59&"
                       f"deletedState=2&publishedState=2&assetTypeID={asset_type_id}&assetClassID={asset_class_id}&"
                       f"districtID={district_id}&includePath=false&includeTaskActuality=true&parentID=-1&"
                       f"tenantID={tenant_id}&isAssigned=false")
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_query_endpoint,
            headers=self.headers.basic_header(token),
            json=self.payloads.post_add_queries_binds_to_user_payload(
                name=name_query,
                query=value_query
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
        assert response.status_code == HTTPStatus.CREATED, f'{response.status_code},{response.json()}'
        model = SuccessAddAssetListQueryModel(result=response.json())
        logger.info(f'Successfully creates a saved queries and binds it to the current user.')
        return model

    @allure.step("Add asset list queries add to user, only asset type.")
    def post_add_asset_list_queries_only_asset_type(
            self,
            token,
            asset_type_id,
            tenant_id
    ):
        name_query = f"Запрос {randint(1, 9999)}"
        value_query = (f"warrantyTill=9999-12-31T23%3A59%3A59&assetTypeID={asset_type_id}&includePath=false"
                       f"&includeTaskActuality=true&parentID=-1&tenantID={tenant_id}&isAssigned=false")
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_query_endpoint,
            headers=self.headers.basic_header(token),
            json=self.payloads.post_add_queries_binds_to_user_payload(
                name=name_query,
                query=value_query
            )
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code},{data_response}'
        model = SuccessAddAssetListQueryModel(result=response.json())
        logger.info(f'Successfully add asset list queries only asset type.')
        return model

    @allure.step("Get a list of stored queries available in the tenant.")
    def get_list_queries_available_in_tenant(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_queries_available_in_tenant_endpoint,
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
            logger.warning("The list of stored queries available in the tenant is not available.")
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessGetAssetListQueryResultModel(root=response.json())
        logger.info(f'Successfully get a list of stored queries available in the tenant.')
        return model

    @allure.step("Get saved query by ID.")
    def get_query_by_id(self, query_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_query_by_id(query_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, f'{response.status_code},{response.json()}'
        model = AssetListQueryResult(**response.json())
        logger.info(f'Successfully get saved query by ID.')
        return model

    @allure.step("Update queries and binds it to the current user.")
    def put_update_queries(self, query_id, tenant_id, token):
        name_query = f"Запрос {randint(100, 199)}"
        value_query = f"warrantyTill=Invalid%20date&deletedState=2&publishedState=2&parentID=-1&tenantID={tenant_id}"
        start = time.time()
        response = requests.put(
            url=self.endpoints.post_add_query_endpoint,
            headers=self.headers.basic_header(token),
            json=self.payloads.put_update_queries_payload(
                query_id=query_id,
                name=name_query,
                query=value_query
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, f'{response.status_code},{response.json()}'
        logger.info(f'Successfully update queries and binds it to the current user.')
        return name_query

    @allure.step("Delete saved queries by list.")
    def delete_saved_queries_by_list(self, query_id: str):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_queries_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_queries_list_payloads(query_id)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, f'{response.status_code},{response.json()}'
        logger.warning(f'Successfully delete saved queries by list.')

    @allure.step("Delete saved query by ID (remove).")
    def delete_saved_query_by_id_remove(self, query_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_remove_query_by_id(query_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, f'{response.status_code},{response.json()}'
        logger.warning(f'Successfully delete saved queries by id (remove).')

    @allure.step("Delete saved query by ID.")
    def delete_saved_query_by_id(self, query_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_query_by_id(query_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, f'{response.status_code},{response.json()}'
        logger.warning(f'Successfully delete saved queries by ID : {query_id}.')

    @allure.step("Delete saved queries by list (remove).")
    def delete_saved_queries_by_list_remove(self, query_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_remove_query_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_queries_list_payloads(query_id)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, f'{response.status_code},{response.json()}'
        logger.warning(f'Successfully delete saved queries by list.')
