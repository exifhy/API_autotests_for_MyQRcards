import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.auth.auth_accounts.payloads import Payloads
from services.auth.auth_accounts.endpoints import Endpoints
from config.headers import Headers
from services.auth.auth_accounts.models.auth_accounts_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from random import randint
from utils.token_utils import get_token
from src.generators.generators import generated_user

load_dotenv()
APP_ID = os.getenv('APP_ID')
USER_EMAIL = os.getenv('USER_EMAIL')


class AuthAccountsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()
        self.user = next(generated_user())

    @allure.step("Account applications without additional parameters.")
    def get_account_applications(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_account_applications_endpoint,
            headers=self.headers.auth_header(bearer_token=get_token(), app_id=APP_ID)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
            logger.warning(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            f'{response.status_code}, {response.json()}'
        model = SuccessGetApplicationListResultModel(result=response.json())
        logger.warning(f'Successfully received account applications without additional parameters.')
        return model

    @allure.step("Account applications with parameters(range).")
    def get_account_applications_with_range(self):
        param_range = {
            'Range': 'items=1-25'
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_account_applications_endpoint,
            headers=self.headers.auth_header(bearer_token=get_token(), app_id=APP_ID, **param_range)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            f'Status code {response.status_code}, {response.json()}'
        model = SuccessGetApplicationListResultModel(result=response.json())
        logger.warning(f'Successfully received account applications with range parameters.')
        return model

    @allure.step("Account applications with parameters(offset, fetch).")
    def get_account_applications_with_offset_fetch(self, offset: str, fetch: str):
        params = {
            "offset": offset,
            "fetch": fetch
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_account_applications_endpoint, params=params,
            headers=self.headers.auth_header(bearer_token=get_token(), app_id=APP_ID)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            f'Status code {response.status_code}, {response.json()}'
        model = SuccessGetApplicationListResultModel(result=response.json())
        logger.warning(f'Successfully received account applications with range parameters.')
        return model

    @allure.step("Account applications without authorization token.")
    def get_account_applications_without_authorization_token(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_account_applications_endpoint,
            headers=self.headers.without_authorization_field_header(APP_ID)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, f'Status code {response.status_code}, {response.json()}'
        model = ErrorModel(list_model=response.json())
        logger.warning(f'Expected error: {model.list_model[0].message}.')
        return model

    @allure.step("Account applications with invalid authorization token.")
    def get_account_applications_with_invalid_authorization_token(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_account_applications_endpoint,
            headers=self.headers.auth_header(bearer_token="InvalidToken", app_id=APP_ID)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, f'Status code {response.status_code}, {response.json()}'
        model = ErrorModel(list_model=response.json())
        logger.warning(f'Expected error: {model.list_model[0].message}.')
        return model

    @allure.step("Account applications with incorrect values in parameters (Range).")
    def get_account_applications_with_incorrect_values_range(self, key: str, value: str):
        params = {
            key: value
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_account_applications_endpoint,
            headers=self.headers.auth_header(bearer_token=get_token(), app_id=APP_ID, **params)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CONFLICT, f'Status code {response.status_code}, {response.json()}'
        model = ErrorModel(list_model=response.json())
        logger.warning(f'Expected error: {model.list_model[0].message}.')
        return model

    @allure.step("Account applications with incorrect values in parameters.")
    def get_account_applications_with_incorrect_values_in_parameters(self, key: str, value: str):
        params = {
            key: value
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_account_applications_endpoint, params=params,
            headers=self.headers.auth_header(bearer_token=get_token(), app_id=APP_ID)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CONFLICT, f'Status code {response.status_code}, {response.json()}'
        model = ErrorModel(list_model=response.json())
        logger.warning(f'Expected error: {response.status_code}, message: {model.list_model[0].message}.')
        return model

    @allure.step("Updating the current account's application data.")
    def put_updating_current_accounts_application_data(self):
        uniq_client_id = str(randint(100000000000000, 999999999999999))
        push_token = f'token{randint(100000000, 999999999)}'
        app_id = 1
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_updating_current_account_application_data_endpoint,
            headers=self.headers.auth_header(bearer_token=get_token(), app_id=APP_ID),
            json=self.payloads.updating_current_accounts_application_data_payload(
                client_id=uniq_client_id,
                push_token=push_token,
                app_id=app_id
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_url(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.warning(f'Successfully updating the current accounts application data.')
        return uniq_client_id, app_id

    @allure.step("Delete the app and device from your current account.")
    def delete_app_and_device_from_your_current_account(self, client_id: str, app_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_unbind_app_device_from_your_current_account_endpoint,
            headers=self.headers.auth_header(bearer_token=get_token(), app_id=APP_ID),
            json=self.payloads.delete_app_and_device_from_account_payload(
                client_id=client_id,
                app_id=app_id
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_url(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.warning(f'Successfully delete the app and device from your current account.')

    @allure.step("Logout. Method can be invoked with an expired token.")
    def post_logout_account(self, client_id: str, app_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_logout_endpoint,
            headers=self.headers.auth_header(bearer_token=get_token(), app_id=APP_ID),
            json=self.payloads.delete_app_and_device_from_account_payload(
                client_id=client_id,
                app_id=app_id
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_url(response.request.body)
        assert response.status_code == HTTPStatus.OK, f'Status code {response.status_code}, {response.json()}'
        logger.warning(f'Successfully logout from your current account.')

    @allure.step("Creates an account with email (if not already created), "
                 "blocks it due to failure to verify the email and sends a notification to Rabbit "
                 "to send an email to the specified email address with a link for verification.")
    def post_accounts_register(self):
        value = {
            "email": self.user.email,
            "mobilePhone": self.user.phone,
            "domainLogin": self.user.username
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_register_endpoint,
            headers=self.headers.auth_header(bearer_token=get_token(), app_id=APP_ID),
            json=self.payloads.post_accounts_register_payload(**value)
        )
        end = time.time()
        logger.info(response.headers)
        logger.info(response.json())
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_url(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        model = SuccessAccountAddResultEntityModel(**response.json())
        logger.warning(f'Successfully creates an account with email (if not already created).')
        return model, value

    @allure.step("Returns account data by credentials.")
    def get_accounts_by_credentials(self):
        params = {
            "credential": USER_EMAIL
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_accounts_endpoint, params=params,
            headers=self.headers.auth_header(bearer_token=get_token(), app_id=APP_ID),
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code != HTTPStatus.OK:
            assert response.status_code == HTTPStatus.CONFLICT, f'Status code {response.status_code}, {response.json()}'
            logger.warning(f'No data with such credentials, status code: {response.status_code}.')
        else:
            assert response.status_code == HTTPStatus.OK, f'Status code {response.status_code}'
            model = SuccessAccountsGetResultModel(**response.json())
            logger.warning(f'Successfully returns account data by credentials.')
            return model

    @allure.step("Checks if the account is present by the specified credentials.")
    def head_accounts_by_credentials(self):
        params = {
            "credential": USER_EMAIL
        }
        start = time.time()
        response = requests.head(
            url=self.endpoints.head_checks_if_account_is_present_by_specified_credentials_endpoint, params=params,
            headers=self.headers.basic_content_type,
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code != HTTPStatus.OK:
            assert response.status_code == HTTPStatus.NOT_FOUND, \
                f'Expected status code {HTTPStatus.NOT_FOUND}, but got {response.status_code}, {response.json()}'
            logger.warning(f'No data with such credentials, status code: {response.status_code}.')
        else:
            assert response.status_code == HTTPStatus.OK, f'Status code {response.status_code}'
            logger.warning(f'Successfully checks if the account is present by the specified credentials.')

    @allure.step("List of notifications from the log.")
    def get_list_notifications_from_log(self):
        # params = {
        #     "offset": 10,
        #     "fetch": 10
        # }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_notifications_from_log_endpoint,
            headers=self.headers.auth_header(bearer_token=get_token(), app_id=APP_ID),
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code != HTTPStatus.OK:
            assert response.status_code == HTTPStatus.NO_CONTENT, \
                f'Expected status code {HTTPStatus.NO_CONTENT}, but got {response.status_code}, {response.json()}'
            logger.warning(f'No data of notifications from the log, status code: {response.status_code}.')
        else:
            assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
                f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {response.json()}'
            model = SuccessNotificationListResultModel(result=response.json())
            logger.warning(f'Successfully list of notifications from the log.')
            return model
