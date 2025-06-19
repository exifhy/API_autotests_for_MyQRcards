import base64
from random import randint
from requests_toolbelt import MultipartEncoder
from PIL import Image
import io
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
TENANT_ID = os.getenv('TENANT_ID')


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
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}, {data_response}'
        model = SuccessUserModel(**response.json())
        logger.info(f'Successfully add a user ID {model.userID} staff name {user_name}')
        return model

    @allure.step("Create multiple staff users (20).")
    def post_create_multiple_staff_users(self, count: int = 20) -> List[int]:
        list_warehouses = []

        for _ in range(count):
            model_user = self.post_add_user_staff()
            list_warehouses.append(model_user.userID)

        return list_warehouses

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
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.warning(f'Successfully delete users with ids: {user_ids}.')

    @allure.step("Delete stuff users by list users.")
    def delete_stuff_users_by_list(self, list_users: list):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_users_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=list_users
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
        logger.warning(f'Successfully delete users with qty ids: {len(list_users)}.')

    @allure.step('Get detail user info.')
    def get_user_info_by_id(self, user_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_user_info_by_id_endpoint(user_id),
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, f'{response.status_code}, {data_response}'
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
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            f'{response.status_code}, {data_response}'
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
        self.attach_response_headers(response.headers)
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
        model = AssetAssignmentListResponse(results=response.json())
        logger.info(f'Successfully get user asset assignments by user ID {user_id}.')
        return model

    @allure.step('Get user asset list queries by user ID.')
    def get_user_asset_list_queries_by_id(self, user_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_user_asset_list_queries_endpoint(user_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}. {data_response}.')
        model = AssetListQueryResponseRootModel(root=response.json())
        logger.info(f'Successfully get user asset list queries by user ID {user_id}.')
        return model

    @allure.step('Get user asset list queries this.')
    def get_user_asset_list_queries_this(self, token):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_asset_queries_to_current_user_endpoint,
            headers=self.headers.basic_header(token)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}. {data_response}.')
        model = AssetListQueryResponseRootModel(root=response.json())
        logger.info(f'Successfully get user asset list queries this.')
        return model

    @allure.step('Get list users short info.')
    def get_list_users_short(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_users_short_list_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}. {data_response}.')
        model = UserShortResultResponseModel(root=response.json())
        logger.info(f'Successfully get list users short info, qty users: {len(model.root)}.')
        return model

    @allure.step('Get non-existent user ID.')
    def get_non_existent_user_id(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_users_short_list_endpoint,
            headers=self.headers.basic_header_with_range(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list of users.")
            return 1
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}. {data_response}.')
        UserShortResultResponseModel(root=response.json())
        qty_items = int(response.headers["Content-Range"].split("/")[-1])
        non_existent = qty_items + 1000
        logger.info(f'Successfully get non-existent user ID {non_existent}.')
        return non_existent

    @allure.step('Head users.')
    def head_users(self):
        start = time.time()
        response = requests.head(
            url=self.endpoints.head_users_endpoint,
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
            (f'Expected status code {HTTPStatus.OK}, '
             f'but got {response.status_code}. {data_response}.')
        logger.info(f'Successfully get head users.')
        return None

    @allure.step('Get users relevance.')
    def get_users_relevance(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_users_relevance_endpoint,
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
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list of users relevance.")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}. {data_response}.')
        model = UserRelevanceResponseModel(root=response.json())
        logger.info(f'Successfully get users relevance.')
        return model

    @allure.step('Get users profile.')
    def get_users_profile(self, token):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_user_profile_endpoint,
            headers=self.headers.basic_header(token)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list of users profile.")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}. {data_response}.')
        model = UserProfileResult(**response.json())
        logger.info(f'Successfully get users profile.')
        return model

    @allure.step("Add by integration user customer.")
    def post_add_by_integration_user_customer(self):
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
            url=self.endpoints.post_add_user_by_integration_endpoint, params=params,
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
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = UserAddByIntegrationModel(**response.json())
        logger.info(f'Successfully add a add by integration user ID {model.userID} customer name {user_name}')
        return model

    @allure.step("Add by integration user staff.")
    def post_add_by_integration_user_staff(self):
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
            url=self.endpoints.post_add_user_by_integration_endpoint, params=params,
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
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = UserAddByIntegrationModel(**response.json())
        logger.info(f'Successfully add a add by integration user ID {model.userID} staff name {user_name}')
        return model

    @allure.step('Change users to customer.')
    def post_change_to_customer_users(self, *user_ids: int or tuple):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_change_to_customer_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_change_status_users_by_list_payload(*user_ids)
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
             f'but got {response.status_code}. {data_response}.')
        model_user = self.get_user_info_by_id(*user_ids)
        assert model_user.isCustomer is True, "The user has not changed to a customer"
        logger.info(f'Successfully change users {user_ids} to customer {model_user.isCustomer}.')

    @allure.step('Change users to stuff.')
    def post_change_to_stuff_users(self, *user_ids: int or tuple):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_change_to_staff_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_change_status_users_by_list_payload(*user_ids)
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
             f'but got {response.status_code}. {data_response}.')
        model_user = self.get_user_info_by_id(*user_ids)
        assert model_user.isCustomer is False, "The user has not changed to a stuff"
        logger.info(f'Successfully change users {user_ids} to stuff {model_user.isTechnician}.')

    @allure.step('Restore user by ID.')
    def put_restore_user_by_id(self, user_id: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_restore_user_endpoint(user_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            (f'Expected status code {HTTPStatus.ACCEPTED}, '
             f'but got {response.status_code}. {data_response}.')
        model_user = self.get_user_info_by_id(user_id)
        assert "deleted" not in model_user.model_fields_set, f"User {user_id} not restore from deleted users"
        logger.info(f'Successfully restore user {user_id}.')

    @allure.step('Restore users by list.')
    def put_restore_users_by_list(self, *user_ids: int or tuple):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_restore_users_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_restore_users_by_list_payload(*user_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            (f'Expected status code {HTTPStatus.ACCEPTED}, '
             f'but got {response.status_code}. {data_response}.')
        for item in user_ids:
            model_user = self.get_user_info_by_id(item)
            assert "deleted" not in model_user.model_fields_set, f"User {item} not restore from deleted users"
            logger.info(f'Successfully restore user {item}.')
        return None

    @allure.step('Resend the invitation to the user.')
    def put_user_resend_invitation(self, user_id: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_resend_user_invitation_endpoint(user_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            (f'Expected status code {HTTPStatus.ACCEPTED}, '
             f'but got {response.status_code}. {data_response}.')
        logger.info(f'Successfully Resend the invitation to the user {user_id}.')
        return None

    @allure.step('Get user permissions ui.')
    def get_user_permission_ui_this(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_current_user_ui_permissions_endpoint,
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
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list of user permissions ui.")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}. {data_response}.')
        model = UserPermissionUiModel(results=response.json())
        logger.info(f'Successfully get user permissions ui.')
        return model

    @allure.step('Get user permissions ext.')
    def get_user_permission_ext_this(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_current_user_ext_permissions_endpoint,
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
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list of user permissions ext.")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}. {data_response}.')
        model = UserPermissionExtModel(results=response.json())
        logger.info(f'Successfully get user permissions ext.')
        return model

    @allure.step('Get user profile by user ID.')
    def get_user_profile_by_user_id(self, user_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_user_profile_by_id_endpoint(user_id),
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
            (f'Expected status code {HTTPStatus.OK}, '
             f'but got {response.status_code}. {data_response}.')
        model = UserProfileResult(**response.json())
        logger.info(f'Successfully get user profile by user ID {user_id}.')
        return model

    @allure.step('Get user profile this.')
    def get_user_profile_this(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_current_user_profile_endpoint,
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
            (f'Expected status code {HTTPStatus.OK}, '
             f'but got {response.status_code}. {data_response}.')
        model = UserProfileResult(**response.json())
        logger.info(f'Successfully get this user profile.')
        return model

    @allure.step("Upload user avatar to server by user ID, data from form.")
    def put_upload_user_avatar_to_server_by_user_id_data_from_form(self, user_id: int):
        file_name = f'generated_image_avatar{randint(1, 999)}.jpeg'
        with io.BytesIO() as image_bytes:
            with Image.new("RGB", (256, 256), color="green") as img:
                img.save(image_bytes, format="JPEG")
                image_bytes.seek(0)  # Перемещаем указатель в начало

            payload = MultipartEncoder(
                fields={
                    'IsPublic': "true", 'IsIgnorePossibleDuplication': "false",
                    'Description': "Avatar",
                    'File': (file_name, image_bytes, 'image/jpeg')
                }
            )
            start = time.time()
            response = requests.put(
                url=self.endpoints.put_upload_user_avatar_from_form_endpoint(user_id),
                headers=self.headers.upload_file_header(get_token(), payload.content_type),
                data=payload
            )
            end = time.time()
            logger.info(response.headers)
            self.attach_response_headers(response.headers)
            data_response = self.response_content(response)
            self.attach_response(data_response)
            self.attach_time(start, end)
            self.attach_url(response.request.url)
            assert response.status_code == HTTPStatus.OK, \
                f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
            model = UserAvatarUploadModel(**response.json())
            logger.info(f'Successfully upload user avatar - {file_name} to server.')
            return model

    @allure.step("Upload this user avatar to server, data from form.")
    def put_upload_this_user_avatar_to_server_data_from_form(self, token):
        file_name = f'generated_image_avatar{randint(9999, 9999)}.jpeg'
        with io.BytesIO() as image_bytes:
            with Image.new("RGB", (256, 256), color="green") as img:
                img.save(image_bytes, format="JPEG")
                image_bytes.seek(0)  # Перемещаем указатель в начало

            payload = MultipartEncoder(
                fields={
                    'IsPublic': "true", 'IsIgnorePossibleDuplication': "false",
                    'Description': "Avatar",
                    'File': (file_name, image_bytes, 'image/jpeg')
                }
            )
            start = time.time()
            response = requests.put(
                url=self.endpoints.put_upload_current_user_avatar_from_form_endpoint,
                headers=self.headers.upload_file_header(token, payload.content_type),
                data=payload
            )
            end = time.time()
            logger.info(response.headers)
            self.attach_response_headers(response.headers)
            data_response = self.response_content(response)
            self.attach_response(data_response)
            self.attach_time(start, end)
            self.attach_url(response.request.url)
            assert response.status_code == HTTPStatus.OK, \
                f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
            model = UserAvatarUploadModel(**response.json())
            logger.info(f'Successfully upload this user avatar - {file_name} to server.')
            return model

    @allure.step("Upload user avatar to server by user ID, data from body.")
    def put_upload_user_avatar_by_user_id_data_from_body(self, user_id: int):
        file_name = f'avatar_from_body{randint(1, 9999)}.jpeg'
        with io.BytesIO() as image_bytes:
            with Image.new("RGB", (500, 500), color="black") as img:
                img.save(image_bytes, format="JPEG")
                image_bytes.seek(0)
                image_base64 = base64.b64encode(image_bytes.read()).decode('utf-8')

            payload = {
                "FileName": file_name,
                "ContentType": "image/jpeg",
                "File": image_base64
            }
            start = time.time()
            response = requests.put(
                url=self.endpoints.put_upload_user_avatar_from_body_endpoint(user_id),
                headers=self.headers.basic_header(get_token()),
                json=payload
            )
            end = time.time()
            logger.info(response.headers)
            self.attach_response_headers(response.headers)
            data_response = self.response_content(response)
            self.attach_response(data_response)
            self.attach_time(start, end)
            self.attach_url(response.request.url)
            assert response.status_code == HTTPStatus.OK, \
                f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
            model = UserAvatarUploadModel(**response.json())
            logger.info(f'Successfully upload user avatar {file_name}, data from body. ID {model.attachmentID}.')
            return model

    @allure.step("Upload this user avatar to server, data from body.")
    def put_upload_this_user_avatar_data_from_body(self, token):
        file_name = f'avatar_from_body{randint(9999, 99999)}.jpeg'
        with io.BytesIO() as image_bytes:
            with Image.new("RGB", (500, 500), color="black") as img:
                img.save(image_bytes, format="JPEG")
                image_bytes.seek(0)
                image_base64 = base64.b64encode(image_bytes.read()).decode('utf-8')

            payload = {
                "FileName": file_name,
                "ContentType": "image/jpeg",
                "File": image_base64
            }
            start = time.time()
            response = requests.put(
                url=self.endpoints.put_upload_current_user_avatar_from_body_endpoint,
                headers=self.headers.basic_header(token),
                json=payload
            )
            end = time.time()
            logger.info(response.headers)
            self.attach_response_headers(response.headers)
            data_response = self.response_content(response)
            self.attach_response(data_response)
            self.attach_time(start, end)
            self.attach_url(response.request.url)
            assert response.status_code == HTTPStatus.OK, \
                f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
            model = UserAvatarUploadModel(**response.json())
            logger.info(f'Successfully upload user avatar {file_name}, data from body. ID {model.attachmentID}.')
            return model

    @allure.step('Delete user avatar by user ID.')
    def delete_user_avatar_by_user_id(self, user_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_user_avatar_endpoint(user_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            (f'Expected status code {HTTPStatus.ACCEPTED}, '
             f'but got {response.status_code}. {data_response}.')
        logger.warning(f'Successfully delete user avatar by user ID {user_id}.')
        return None

    @allure.step('Delete this user avatar.')
    def delete_this_user_avatar(self, token):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_current_user_avatar_endpoint,
            headers=self.headers.basic_header(token)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            (f'Expected status code {HTTPStatus.ACCEPTED}, '
             f'but got {response.status_code}. {data_response}.')
        logger.warning(f'Successfully delete this user avatar.')
        return None

    @allure.step('Delete users avatar by list.')
    def delete_users_avatar_by_list(self, *users_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_users_avatar_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_users_avatar_by_list_payload(*users_ids)
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
             f'but got {response.status_code}. {data_response}.')
        logger.warning(f'Successfully delete users avatars by ID {users_ids}.')
        return None

    @allure.step('Get user ratings by ID.')
    def get_user_ratings_by_id(self, user_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_user_ratings_endpoint(user_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}. {data_response}.')
        model = RatingTechnicianResultModel(**response.json())
        logger.warning(f'Successfully Get user ratings by ID {user_id}.')
        return model

    @allure.step("Allows any user to register by invitation ID.")
    def post_add_users_registration(self, invitation_id: str):
        user = next(generated_user())
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_user_registration_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_users_registration_payload(
                invitation_id, user.name, user.surname, user.email
            )
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
        model = UserRegistrationWithInvitationResponseModel(**response.json())
        logger.info(f'Successfully Allows any user to register by invitation ID {invitation_id}')
        return model

    @allure.step("Verify any user to register.")
    def post_add_users_registration_verify(self, account_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_user_registration_verify_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_users_registration_verify_payload(
                TENANT_ID, account_id
            )
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
        model = UserRegistrationVerifyResponseModel(**response.json())
        logger.info(f'Successfully verify any user to register.')
        return model

    @allure.step("Get users skills by user ID.")
    def get_user_skills_by_user_id(self, user_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_user_skills_endpoint(user_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}. {data_response}.')
        model = UserSkillsResponseModel(root=response.json())
        logger.info(f'Successfully get users skills by user ID {user_id}.')
        return model

    @allure.step("Get users tags by user ID.")
    def get_user_tags_by_user_id(self, user_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_user_tags_endpoint(user_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}. {data_response}.')
        model = UserTagsResponseModel(results=response.json())
        logger.info(f'Successfully get users tags by user ID {user_id}.')
        return model

    @allure.step('Get a list task queries to the this user.')
    def get_list_task_queries_to_this_user(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_current_user_task_list_queries_endpoint,
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
            logger.warning("Not available to the user a list task queries.")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}. {data_response}.')
        model = UserTaskListQueryResponse(root=response.json())
        logger.info(f'Successfully get a list task queries to the current user.')
        return model

    @allure.step('Get a list task queries to the user by ID.')
    def get_list_task_queries_to_user_by_id(self, user_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_user_task_list_queries_endpoint(user_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}. {data_response}.')
        model = UserTaskListQueryResponse(root=response.json())
        logger.info(f'Successfully get a list task queries to the user ID {user_id}, qty {len(model.root)}.')
        return model

    @allure.step('Get a list user task queries (204 NO CONTENT).')
    def get_list_task_queries_to_user_by_id_no_content(self, user_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_user_task_list_queries_endpoint(user_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.NO_CONTENT, \
            (f'Expected status code {HTTPStatus.NO_CONTENT}, '
             f'but got {response.status_code}. {data_response}.')
        logger.warning(f'Successfully get a list task queries to the user ID {user_id}, NO CONTENT.')
        return None

    @allure.step('Get a list notifications to the current user.')
    def get_list_notifications_to_current_user(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_current_user_notifications_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}. {data_response}.')
        model = UserDisabledNotificationsListResult(**response.json())
        logger.info(f'Successfully get a list notifications to the current user.')
        return model

    @allure.step('Get a list users warehouses.')
    def get_list_users_warehouses_by_id(self, user_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_users_warehouses_by_user_id_endpoint(user_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}. {data_response}.')
        model = UsersWarehousesResponseModel(results=response.json())
        logger.info(f'Successfully get a list users ID {user_id} warehouses.')
        return model
