import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.adm.adm_default_pages.payloads import Payloads
from services.adm.adm_default_pages.endpoints import Endpoints
from config.headers import Headers
from services.adm.adm_default_pages.models.adm_default_pages_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token
from utils.env import get_app_id
import concurrent.futures


class AdmDefaultPagesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get list default pages.")
    def get_list_default_pages(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_default_pages_endpoint,
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.success(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            (f'Expected status code {HTTPStatus.OK}, '
             f'but got {response.status_code}, {data_response}')
        model = SuccessGetDefaultPagesModel(results=response.json())
        logger.success(f'Successfully get list default pages.')
        return model, response
    
    @allure.step("Get list default pages without token.")
    def get_list_default_pages_without_token(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_default_pages_endpoint,
            headers=self.headers.without_authorization_field_header(get_app_id()),
        )
        end = time.time()
        logger.success(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, \
            (f'Expected status code {HTTPStatus.UNAUTHORIZED}, '
             f'but got {response.status_code}, {data_response}')
        logger.success(f'Successfully verified unauthorized access.')
        return response

    @allure.step("Get list default pages with invalid token.")
    def get_list_default_pages_invalid_token(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_default_pages_endpoint,
            headers=self.headers.basic_header('invalid_token'),
        )
        end = time.time()
        logger.success(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, \
            (f'Expected status code {HTTPStatus.UNAUTHORIZED}, '
             f'but got {response.status_code}, {data_response}')
        logger.success(f'Successfully verified invalid token handling.')
        return response

    @allure.step("Get list default pages with invalid app id.")
    def get_list_default_pages_invalid_app_id(self):
        start = time.time()
        expected_message = "Не найден обязательный заголовок [X-Application-ID]."
        response = requests.get(
            url=self.endpoints.get_list_default_pages_endpoint,
            headers=self.headers.auth_header(get_token(), "invalid app id"),
        )
        end = time.time()
        logger.success(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            (f'Expected status code {HTTPStatus.FORBIDDEN}, '
             f'but got {response.status_code}, {data_response}')
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].message == expected_message, \
            f"Expected {expected_message}, but got {model.list_model[0].message}"
        logger.success(f'Successfully verified invalid app id handling.')
        return model, response

    @allure.step("Get list default pages with content type {content_type}.")
    def get_list_default_pages_with_content_type(self, content_type):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_default_pages_endpoint,
            headers=self.headers.basic_header_content_type(get_token(), content_type),
        )
        end = time.time()
        logger.success(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            (f'Expected status code {HTTPStatus.OK}, '
             f'but got {response.status_code}, {data_response}')
        model = SuccessGetDefaultPagesModel(results=response.json())
        logger.success(f'Successfully get list default pages with content type {content_type}.')
        return model, response

    @allure.step("Get list default pages measure response time.")
    def get_list_default_pages_measure_time(self, threshold_ms=2000):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_default_pages_endpoint,
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        response_time_ms = (end - start) * 1000
        logger.success(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response_time_ms < threshold_ms, \
            (f'Response time {response_time_ms:.2f}ms exceeds threshold {threshold_ms}ms')
        assert response.status_code == HTTPStatus.OK, \
            (f'Expected status code {HTTPStatus.OK}, '
             f'but got {response.status_code}, {data_response}')
        model = SuccessGetDefaultPagesModel(results=response.json())
        logger.success(f'Successfully measured response time: {response_time_ms:.2f}ms')
        return model, response

    @allure.step("Get list default pages idempotency.")
    def get_list_default_pages_idempotent(self):
        start = time.time()
        response1 = requests.get(
            url=self.endpoints.get_list_default_pages_endpoint,
            headers=self.headers.basic_header(get_token()),
        )
        response2 = requests.get(
            url=self.endpoints.get_list_default_pages_endpoint,
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.success(response1.headers)
        logger.success(response2.headers)
        self.attach_response_headers(response1.headers)
        self.attach_response_headers(response2.headers)
        data_response1 = self.response_content(response1)
        data_response2 = self.response_content(response2)
        self.attach_response(data_response1)
        self.attach_response(data_response2)
        self.attach_time(start, end)
        self.attach_url(response1.request.url)
        
        assert response1.status_code == response2.status_code, \
            (f'Status codes differ: {response1.status_code} vs {response2.status_code}')
        
        if response1.status_code == HTTPStatus.OK and response2.status_code == HTTPStatus.OK:
            assert response1.json() == response2.json(), "Responses differ between requests"
        
        assert response1.status_code == HTTPStatus.OK, \
            (f'Expected status code {HTTPStatus.OK}, '
             f'but got {response1.status_code}, {data_response1}')
        
        model = SuccessGetDefaultPagesModel(results=response1.json())
        logger.success(f'Successfully verified idempotency.')
        return model, response1

    @allure.step("Get list default pages concurrent requests.")
    def get_list_default_pages_concurrent(self, num_requests=10):
        def make_request():
            return requests.get(
                url=self.endpoints.get_list_default_pages_endpoint,
                headers=self.headers.basic_header(get_token()),
            )
        
        start = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
            futures = [executor.submit(make_request) for _ in range(num_requests)]
            responses = [future.result() for future in futures]
        end = time.time()
        success_count = sum(1 for r in responses if r.status_code == HTTPStatus.OK)
        self.attach_time(start, end)
        assert success_count == num_requests, \
            (f'Not all requests succeeded. Status codes: {[r.status_code for r in responses]}')
        
        logger.success(f'Successfully completed {num_requests} concurrent requests. '
                   f'OK: {success_count}')
        return responses

    @allure.step("Get list default pages verify forbidden access.")
    def get_list_default_pages_forbidden(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_default_pages_endpoint,
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.success(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        
        assert response.status_code != HTTPStatus.FORBIDDEN, \
            (f'Got unexpected forbidden status code {HTTPStatus.FORBIDDEN}, '
             f'but should have access, {data_response}')
        
        logger.success(f'Successfully verified access is not forbidden.')
        return response
