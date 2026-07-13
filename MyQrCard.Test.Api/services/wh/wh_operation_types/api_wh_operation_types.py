import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.wh.wh_operation_types.payloads import Payloads
from services.wh.wh_operation_types.endpoints import Endpoints
from config.headers import Headers
from services.wh.wh_operation_types.models.wh_operation_types_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token
from random import randint


class WhOperationTypesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get operation type by ID.")
    def get_operation_type_by_id(self, type_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_operation_types_by_id_endpoint(type_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessGetOperationTypeResult(**response.json())
        logger.info(f'Successfully get operation type by ID {model.id}')
        return model

    @allure.step("Delete operation type by ID.")
    def delete_operation_type_by_id(self, type_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_operation_types_by_id_endpoint(type_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.info(f'Successfully delete operation type by ID {type_id}')
        return None

    @allure.step("Get list operation types.")
    def get_list_operation_types(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_operation_types_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, but got {response.status_code}, {data_response}'
        model = SuccessGetListOperationTypeResult(root=response.json())
        logger.info(f'Successfully get list operation types.')
        return model

    @allure.step("Post operation types.")
    def post_operation_type(self, doc_type_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_operation_types_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_operation_type_payload(
                name=f"Operation Type {randint(1000, 9999)}",
                doc_type_id=doc_type_id,
                erp_id=f"OTErpID {randint(10000, 99999)}"
            )
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessOperationTypeAddResultModel(results=response.json())
        logger.info(f'Successfully post operation types ID {model.results[0].id}.')
        return model

    @allure.step("Put update operation type.")
    def put_operation_type(self, doc_type_id: int, type_id: int):
        model_before = self.get_operation_type_by_id(type_id)
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_operation_types_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_operation_type_payload(
                name=f"Update Operation Type {randint(1000, 9999)}",
                doc_type_id=doc_type_id,
                erp_id=f"OTErpID {randint(100000, 999999)}",
                type_id=type_id
            )
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.info(f'Successfully update operation type ID {type_id}.')
        model_after = self.get_operation_type_by_id(type_id)
        assert model_before != model_after, f'Operation type ID {type_id} not updated'
        return None

    @allure.step("Delete operation types by list.")
    def delete_operation_types_by_list(self, *type_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_operation_types_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=[*type_ids]
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.info(f'Successfully delete operation types by list {type_ids}')
        return None
