import random
import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from src.generators.generators import generated_user
from services.adm.users.payloads import Payloads
from services.adm.users.endpoints import Endpoints
from config.headers import Headers
from services.adm.users.models.adm_users_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token
from dotenv import load_dotenv
import os


load_dotenv()
APP_ID = os.getenv('APP_ID')


class AdmUsersAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()
        # self.user = next(generated_user())

    @allure.step("Add user customer.")
    def post_add_user_customer(self):
        """Заказчик"""
        user = next(generated_user())
        params = {
            "skipAccountVerification": True
        }
        user_name = user.name
        user_surname = user.surname
        user_email = user.email
        user_phone = user.phone
        start = time.time()
        response = requests.post(
            url=self.endpoints.add_users_endpoint, params=params,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.add_user_customer_payload(
                name=user_name,
                surname=user_surname,
                email=user_email,
                phone=user_phone
            )
        )
        end = time.time()
        logger.info(response.headers)
        logger.warning(response.request.url)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessUserModel(**response.json())
        logger.info(f'Successfully add a user customer name: {user_name}')
        return model

    @allure.step("Add user staff is technician.")
    def post_add_user_staff(self):
        """Сотрудник"""
        user = next(generated_user())
        params = {
            "skipAccountVerification": True
        }
        user_name = user.name
        user_surname = user.surname
        user_email = user.email
        user_phone = user.phone
        start = time.time()
        response = requests.post(
            url=self.endpoints.add_users_endpoint, params=params,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.add_user_staff_payload(
                name=user_name,
                surname=user_surname,
                email=user_email,
                phone=user_phone
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}, {response.json()}'
        model = SuccessUserModel(**response.json())
        logger.info(f'Successfully add a user ID {model.userID} staff name {user_name}')
        return model

    @allure.step("Delete user by ID.")
    def delete_user_by_id(self, user_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_user_by_id_endpoint(user_id),
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}. but got {response.status_code}, {response.json()}'
        logger.warning(f'Successfully delete user with id: {user_id}.')

    @allure.step("Delete users by list.")
    def delete_users_by_list(self, *user_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_users_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_users_by_list_payload(*user_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.warning(f'Successfully delete users with ids: {user_ids}.')

    @allure.step('Get detail user info.')
    def get_user_info_by_id(self, user_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_user_info_by_id_endpoint(user_id),
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, f'{response.status_code}, {response.json()}'
        model = SuccessGetDetailedInfoUserModel(**response.json())
        logger.info(f'Successfully received detail user info.')
        return model

    @allure.step('Get list users info.')
    def get_list_users_info(self):
        # params = {
        #     "searchText": str,
        #     "includeTaskActuality": bool,
        #     "includeDistricts": bool,
        #     "needForAllowedTasks": bool
        # }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_users_endpoint,
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            f'{response.status_code}, {response.json()}'
        model = SuccessGetUsersListModel(**response.json())
        logger.info(f'Successfully received list users info.')
        return model

    @allure.step('Get list users return ids.')
    def get_list_users_ids(self):
        list_users = []
        params = {
            "isCustomer": False,
            "includeTaskActuality": True,
            "isDeleted": False,
            # "needForAllowedTasks": bool
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_users_endpoint, params=params,
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.info(response.headers)
        # self.attach_response_headers(response)
        # data_response = self.response_content(response)
        self.attach_response(response.json())
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, but got {response.status_code}, '
             f'{response.json()}')
        model = SuccessGetUsersListModel(**response.json())
        for ids, data in model.root.items():
            int_id = int(ids)
            list_users.append(int_id)
        logger.info(f'Successfully get list {list_users} users.')
        return list_users

    @allure.step("Put update user.")
    def put_update_user_by_id(self, user_id: int, user_email: str, user_phone: str):
        user = next(generated_user())
        sex = random.randint(1, 3)
        new_user_name = user.name
        new_user_surname = user.surname
        new_user_email = user.email
        new_user_phone = user.phone
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_user_info_by_id_endpoint(user_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_user_payload(
                name=new_user_name,
                surname=new_user_surname,
                email=new_user_email,
                phone=new_user_phone,
                sex=sex,
                old_phone=user_phone,
                old_mail=user_email
            )
        )
        end = time.time()
        logger.info(response.headers)
        logger.warning(response.request.url)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, f'{response.status_code}, {response.json()}'
        model = self.get_user_info_by_id(user_id)
        assert model.firstName == new_user_name, f'Expected {model.firstName}, but got {new_user_name}.'
        assert model.lastName == new_user_surname, f'Expected {model.lastName}, but got {new_user_surname}.'
        assert model.email == new_user_email, f'Expected {model.email}, but got {new_user_email}.'
        assert model.mobilePhone == new_user_phone, f'Expected {model.mobilePhone}, but got {new_user_phone}.'
        assert model.sex.id == sex, f'Expected {model.sex.id}, but got {sex}.'
        logger.info(f'Successfully update a user by userID: {user_id}')

    @allure.step("Creates an API user in the tenant.")
    def post_add_api_user_in_tenant(self, access_token: str):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_api_user_in_tenant_endpoint,
            headers=self.headers.authorization_header(access_token, APP_ID)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, f'{response.status_code}, {response.json()}'
        model = SuccessCreatedApiUserModel(**response.json())
        logger.info(f'Successfully add an API user in the tenant.')
        return model

    @allure.step('Get users roles by ID.')
    def get_users_roles_by_id(self, user_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_users_roles_by_id_endpoint(user_id),
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}.'
        model = SuccessGetUsersRolesModel(root=response.json())
        logger.info(f'Successfully received users roles by ID.')
        return model

    @allure.step('Get a list asset queries to the current user.')
    def get_list_asset_queries_to_current_user(self, token):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_asset_queries_to_current_user_endpoint,
            headers=self.headers.basic_header(token)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning("Not available to the user a list asset queries.")
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}.'
        model = AssetListQueryResultModel(**response.json())
        logger.info(f'Successfully get a list asset queries to the current user.')
        return model

    @allure.step('Add anonymous user.')
    def post_add_anonymous_user(self):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_anonymous_user_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}. {data_response}.'
        model = SuccessCreatedApiUserModel(**response.json())
        logger.info(f'Successfully add anonymous user.')
        return model

    @allure.step('Get user notifications by user ID.')
    def get_user_notifications_by_id(self, user_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_user_notifications_endpoint(user_id),
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
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}.'
        model = UserDisabledNotificationsListResult(**response.json())
        logger.info(f'Successfully get user notifications by user ID {user_id}.')
        return model

    @allure.step('Get user districts by user ID.')
    def get_user_districts_by_id(self, user_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_user_districts_endpoint(user_id),
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
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}.'
        model = SuccessGetUsersDistrictsModel(root=response.json())
        logger.info(f'Successfully get user districts by user ID {user_id}.')
        return model

    @allure.step('Get user asset assignments by user ID.')
    def get_user_asset_assignments_by_id(self, user_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_user_asset_assignments_endpoint(user_id),
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
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}.'
        model = SuccessGetUsersDistrictsModel(root=response.json())
        logger.info(f'Successfully get user districts by user ID {user_id}.')
        return model
