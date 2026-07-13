import allure
import requests
from loguru import logger
from utils.helper import Helper
from utils.token_utils import get_token
from services.wh.wh_user_warehouses.payloads import Payloads
from services.wh.wh_user_warehouses.endpoints import Endpoints
from config.headers import Headers
from services.wh.wh_user_warehouses.models.wh_user_warehouses_model import *
import time
from http import HTTPStatus


class WhUserWarehousesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get list of user warehouses.")
    def get_list_of_user_warehouses(self, user_id):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_user_warehouses_endpoint(user_id),
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
        model = UserWarehousesListResponseModel(results=response.json())
        logger.info(f'Successfully get list of user warehouses, qty {len(model.results)}.')
        return model

    @allure.step("Add multiple warehouses to the user, by user ID.")
    def post_add_multiple_warehouses_to_user_by_user_id(self, user_id, *wh_ids: int or tuple):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_multiple_warehouses_to_user_endpoint(user_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_warehouses_to_user_payload(*wh_ids)
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
             f'but got {response.status_code}. {data_response}.')
        model = UserWarehousesAddListResponseModel(root=response.json())
        logger.info(f'Successfully add multiple warehouses ID {wh_ids} to the user ID {user_id}.')
        return model

    @allure.step("Add list warehouses to the user, by user ID.")
    def post_add_list_warehouses_to_user_by_user_id(self, user_id, list_whs: list):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_multiple_warehouses_to_user_endpoint(user_id),
            headers=self.headers.basic_header(get_token()),
            json=list_whs
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
             f'but got {response.status_code}. {data_response}.')
        model = UserWarehousesAddListResponseModel(root=response.json())
        logger.info(f'Successfully add list warehouses qty IDs {len(list_whs)} to the user ID {user_id}.')
        return model

    @allure.step("Delete multiple warehouses from user, by user ID.")
    def delete_multiple_warehouses_from_user_by_user_id(self, user_id, *wh_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_multiple_warehouses_from_user_endpoint(user_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_multiple_warehouses_from_user_payload(*wh_ids)
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
        logger.warning(f'Successfully delete multiple warehouses ID {wh_ids} from user ID {user_id}.')
        return None

    @allure.step("Add multiple warehouses to the users.")
    def post_add_multiple_warehouses_to_users(self, user_ids: list, warehouse_ids_list: list):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_multiple_warehouses_to_users_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_warehouses_to_users_payload(user_ids, warehouse_ids_list)
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
             f'but got {response.status_code}. {data_response}.')
        model = UserWarehousesAddListResponseModel(root=response.json())
        logger.info(f'Successfully add multiple warehouses ID {len(warehouse_ids_list)} to the users ID {user_ids}.')
        return model

    @allure.step("Delete multiple warehouses from users.")
    def delete_multiple_warehouses_from_users(self, user_ids: list, warehouse_ids_list: list):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_multiple_warehouses_from_users_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_multiple_warehouses_from_users_payload(user_ids, warehouse_ids_list)
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
        logger.warning(f'Successfully delete multiple warehouses qty IDs '
                       f'{len(warehouse_ids_list)} from users qty IDs {len(user_ids)}.')
        return None

    @allure.step("Add deleted warehouse to the user, by user ID.")
    def post_add_deleted_warehouse_to_user_by_user_id(self, user_id, *wh_ids: int or tuple):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_multiple_warehouses_to_user_endpoint(user_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_warehouses_to_user_payload(*wh_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CONFLICT, \
            (f'Expected status code {HTTPStatus.CONFLICT}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_warehouse_deleted(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add warehouse to deleted user, by user ID.")
    def post_add_warehouse_to_deleted_user_by_user_id(self, user_id, *wh_ids: int or tuple):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_multiple_warehouses_to_user_endpoint(user_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_warehouses_to_user_payload(*wh_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            (f'Expected status code {HTTPStatus.FORBIDDEN}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_user_deleted(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add non-existent warehouse to user, by user ID.")
    def post_add_non_existent_warehouse_to_user_by_user_id(self, user_id, *wh_ids: int or tuple):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_multiple_warehouses_to_user_endpoint(user_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_warehouses_to_user_payload(*wh_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            (f'Expected status code {HTTPStatus.NOT_FOUND}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_warehouse_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add warehouse to non-existent user.")
    def post_add_warehouse_to_non_existent_user(self, user_id, *wh_ids: int or tuple):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_multiple_warehouses_to_user_endpoint(user_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_warehouses_to_user_payload(*wh_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            (f'Expected status code {HTTPStatus.FORBIDDEN}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_user_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add deleted and valid warehouses to valid user, by user ID.")
    def post_add_deleted_and_valid_warehouses_to_user(self, user_id, *wh_ids: int or tuple):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_multiple_warehouses_to_user_endpoint(user_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_warehouses_to_user_payload(*wh_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CONFLICT, \
            (f'Expected status code {HTTPStatus.CONFLICT}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_warehouse_deleted(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add deleted and non-existent warehouses to valid user, by user ID.")
    def post_add_deleted_and_non_existent_warehouses_to_user(self, user_id, *wh_ids: int or tuple):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_multiple_warehouses_to_user_endpoint(user_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_warehouses_to_user_payload(*wh_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            (f'Expected status code {HTTPStatus.NOT_FOUND}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_warehouse_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add already added warehouse to valid user, by user ID.")
    def post_add_already_added_warehouse_to_user(self, user_id, *wh_ids: int or tuple):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_multiple_warehouses_to_user_endpoint(user_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_warehouses_to_user_payload(*wh_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CONFLICT, \
            (f'Expected status code {HTTPStatus.CONFLICT}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_already_done(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add unavailable warehouse to user, role without permission <Все склады>.")
    def post_unavailable_warehouse_to_user(self, token, user_id, *wh_ids: int or tuple):
        """У пользователя роль без полномочия <Все склады>, добавляется склад недоступный для пользователя."""
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_multiple_warehouses_to_user_endpoint(user_id),
            headers=self.headers.basic_header(token),
            json=self.payloads.post_add_multiple_warehouses_to_user_payload(*wh_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            (f'Expected status code {HTTPStatus.FORBIDDEN}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].code == "AccessDenied", \
            f'Expected <AccessDenied>, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "Доступ запрещён: Указанный склад", \
            f'Expected <Доступ запрещён: Указанный склад>, but got {model.list_model[0].message}'
        assert "AccessDenied" in response.headers["X-Application-Errors"], \
            f'Expected <AccessDenied>, but got {response.headers["X-Application-Errors"]}'
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add warehouse to unavailable user.")
    def post_warehouse_to_unavailable_user(self, token, user_id, *wh_ids: int or tuple):
        """Пользователь с ролью без полномочия <Пользователи и контакты> добавляет другому пользователю склад."""
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_multiple_warehouses_to_user_endpoint(user_id),
            headers=self.headers.basic_header(token),
            json=self.payloads.post_add_multiple_warehouses_to_user_payload(*wh_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            (f'Expected status code {HTTPStatus.FORBIDDEN}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].code == "AccessDenied", \
            f'Expected <AccessDenied>, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "Доступ запрещён: Обрабатываемый пользователь", \
            f'Expected <Доступ запрещён: Обрабатываемый пользователь>, but got {model.list_model[0].message}'
        assert "AccessDenied" in response.headers["X-Application-Errors"], \
            f'Expected <AccessDenied>, but got {response.headers["X-Application-Errors"]}'
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add deleted warehouse to the users.")
    def post_add_deleted_warehouse_to_users(self, user_ids: list, warehouse_ids_list: list):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_multiple_warehouses_to_users_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_warehouses_to_users_payload(user_ids, warehouse_ids_list)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CONFLICT, \
            (f'Expected status code {HTTPStatus.CONFLICT}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_warehouse_deleted(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add warehouse to deleted users.")
    def post_add_warehouse_to_deleted_users(self, user_ids: list, warehouse_ids_list: list):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_multiple_warehouses_to_users_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_warehouses_to_users_payload(user_ids, warehouse_ids_list)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            (f'Expected status code {HTTPStatus.FORBIDDEN}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_user_deleted(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add non-existent warehouse to users.")
    def post_add_non_existent_warehouse_to_users(self, user_ids: list, warehouse_ids_list: list):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_multiple_warehouses_to_users_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_warehouses_to_users_payload(user_ids, warehouse_ids_list)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            (f'Expected status code {HTTPStatus.NOT_FOUND}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_warehouse_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add warehouse to list non-existent user.")
    def post_add_warehouse_to_list_non_existent_user(self, user_ids: list, warehouse_ids_list: list):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_multiple_warehouses_to_users_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_warehouses_to_users_payload(user_ids, warehouse_ids_list)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            (f'Expected status code {HTTPStatus.FORBIDDEN}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_user_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add valid and deleted warehouses to list user.")
    def post_add_valid_and_deleted_warehouses_to_list_user(self, user_ids: list, warehouse_ids_list: list):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_multiple_warehouses_to_users_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_warehouses_to_users_payload(user_ids, warehouse_ids_list)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CONFLICT, \
            (f'Expected status code {HTTPStatus.CONFLICT}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_warehouse_deleted(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add valid and non-existent warehouses to list user.")
    def post_add_valid_and_non_existent_warehouses_to_list_user(self, user_ids: list, warehouse_ids_list: list):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_multiple_warehouses_to_users_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_warehouses_to_users_payload(user_ids, warehouse_ids_list)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            (f'Expected status code {HTTPStatus.NOT_FOUND}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_warehouse_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add deleted and non-existent warehouses to list user.")
    def post_add_deleted_and_non_existent_warehouses_to_list_user(self, user_ids: list, warehouse_ids_list: list):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_multiple_warehouses_to_users_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_warehouses_to_users_payload(user_ids, warehouse_ids_list)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            (f'Expected status code {HTTPStatus.NOT_FOUND}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_warehouse_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add valid warehouse to valid and deleted users.")
    def post_add_valid_warehouse_to_valid_and_deleted_users(self, user_ids: list, warehouse_ids_list: list):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_multiple_warehouses_to_users_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_warehouses_to_users_payload(user_ids, warehouse_ids_list)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            (f'Expected status code {HTTPStatus.FORBIDDEN}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_user_deleted(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add valid warehouse to valid and non-existent users.")
    def post_add_valid_warehouse_to_valid_and_non_existent_users(self, user_ids: list, warehouse_ids_list: list):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_multiple_warehouses_to_users_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_warehouses_to_users_payload(user_ids, warehouse_ids_list)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            (f'Expected status code {HTTPStatus.FORBIDDEN}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_user_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add deleted and non-existent warehouses to two valid users.")
    def post_add_deleted_and_non_existent_warehouse_to_two_valid_users(self, user_ids: list, warehouse_ids_list: list):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_multiple_warehouses_to_users_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_warehouses_to_users_payload(user_ids, warehouse_ids_list)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            (f'Expected status code {HTTPStatus.NOT_FOUND}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_warehouse_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add valid, deleted and non-existent warehouses to valid user.")
    def post_add_valid_deleted_and_non_existent_warehouse_to_valid_user(self, user_ids: list, warehouse_ids_list: list):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_multiple_warehouses_to_users_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_warehouses_to_users_payload(user_ids, warehouse_ids_list)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            (f'Expected status code {HTTPStatus.NOT_FOUND}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_warehouse_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add already added warehouse to valid user.")
    def post_add_already_added_warehouse_to_valid_user(self, user_ids: list, warehouse_ids_list: list):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_multiple_warehouses_to_users_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_warehouses_to_users_payload(user_ids, warehouse_ids_list)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CONFLICT, \
            (f'Expected status code {HTTPStatus.CONFLICT}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_already_done(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add unavailable warehouse to list user, role without permission <Все склады>.")
    def post_add_unavailable_warehouse_to_list_user(self, token, user_ids: list, warehouse_ids_list: list):
        """У пользователя роль без полномочия <Все склады>, добавляется склад недоступный для пользователя."""
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_multiple_warehouses_to_users_endpoint,
            headers=self.headers.basic_header(token),
            json=self.payloads.post_add_multiple_warehouses_to_users_payload(user_ids, warehouse_ids_list)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            (f'Expected status code {HTTPStatus.FORBIDDEN}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].code == "AccessDenied", \
            f'Expected <AccessDenied>, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "Доступ запрещён: Указанный склад", \
            f'Expected <Доступ запрещён: Указанный склад>, but got {model.list_model[0].message}'
        assert "AccessDenied" in response.headers["X-Application-Errors"], \
            f'Expected <AccessDenied>, but got {response.headers["X-Application-Errors"]}'
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add warehouse to unavailable list user.")
    def post_add_warehouse_to_unavailable_list_user(self, token, user_ids: list, warehouse_ids_list: list):
        """Пользователь с ролью без полномочия <Пользователи и контакты> добавляет другому пользователю склад."""
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_multiple_warehouses_to_users_endpoint,
            headers=self.headers.basic_header(token),
            json=self.payloads.post_add_multiple_warehouses_to_users_payload(user_ids, warehouse_ids_list)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            (f'Expected status code {HTTPStatus.FORBIDDEN}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].code == "AccessDenied", \
            f'Expected <AccessDenied>, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "Доступ запрещён: Обрабатываемый пользователь", \
            f'Expected <Доступ запрещён: Обрабатываемый пользователь>, but got {model.list_model[0].message}'
        assert "AccessDenied" in response.headers["X-Application-Errors"], \
            f'Expected <AccessDenied>, but got {response.headers["X-Application-Errors"]}'
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add empty list warehouses to owner user.")
    def post_add_empty_list_warehouses_to_owner_user(self):
        data = [
            {
                "userID": 1,
                "warehouseIDs": []
            }
        ]
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_multiple_warehouses_to_users_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=data
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.NO_CONTENT, \
            (f'Expected status code {HTTPStatus.NO_CONTENT}, '
             f'but got {response.status_code}. {data_response}.')
        logger.warning(f'Expected result: status code {response.status_code}.')
        return None

    @allure.step("Add warehouses to users, send empty list.")
    def post_add_warehouses_to_user_send_empty_list(self):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_multiple_warehouses_to_users_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=[]
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CONFLICT, \
            (f'Expected status code {HTTPStatus.CONFLICT}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].code == "ParameterNull", \
            f'Expected <ParameterNull>, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "Параметр [data] не может быть пустым.", \
            f'Expected <Параметр [data] не может быть пустым.>, but got {model.list_model[0].message}'
        assert "ParameterNull" in response.headers["X-Application-Errors"], \
            f'Expected <ParameterNull>, but got {response.headers["X-Application-Errors"]}'
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}')
        return None

    @allure.step("Delete already deleted warehouse from user, by user ID.")
    def delete_already_deleted_warehouse_from_user_by_user_id(self, user_id, *wh_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_multiple_warehouses_from_user_endpoint(user_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_multiple_warehouses_from_user_payload(*wh_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CONFLICT, \
            (f'Expected status code {HTTPStatus.CONFLICT}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_already_done(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete deleted from system warehouse from user, by user ID.")
    def delete_deleted_from_system_warehouse_from_user_by_user_id(self, user_id, *wh_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_multiple_warehouses_from_user_endpoint(user_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_multiple_warehouses_from_user_payload(*wh_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CONFLICT, \
            (f'Expected status code {HTTPStatus.CONFLICT}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_warehouse_deleted(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete warehouse from deleted user, by user ID.")
    def delete_warehouse_from_deleted_user_by_user_id(self, user_id, *wh_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_multiple_warehouses_from_user_endpoint(user_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_multiple_warehouses_from_user_payload(*wh_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            (f'Expected status code {HTTPStatus.FORBIDDEN}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_user_deleted(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete deleted and valid warehouses from user, by user ID.")
    def delete_deleted_and_valid_warehouses_from_user_by_user_id(self, user_id, *wh_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_multiple_warehouses_from_user_endpoint(user_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_multiple_warehouses_from_user_payload(*wh_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CONFLICT, \
            (f'Expected status code {HTTPStatus.CONFLICT}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_warehouse_deleted(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete valid warehouse from non-existent user, by user ID.")
    def delete_valid_warehouse_from_non_existent_user(self, user_id, *wh_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_multiple_warehouses_from_user_endpoint(user_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_multiple_warehouses_from_user_payload(*wh_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            (f'Expected status code {HTTPStatus.FORBIDDEN}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_user_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete non-existent warehouse from non-existent user, by user ID.")
    def delete_non_existent_warehouse_from_non_existent_user(self, user_id, *wh_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_multiple_warehouses_from_user_endpoint(user_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_multiple_warehouses_from_user_payload(*wh_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            (f'Expected status code {HTTPStatus.NOT_FOUND}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_warehouse_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete non-existent warehouse from valid user, by user ID.")
    def delete_non_existent_warehouse_from_valid_user(self, user_id, *wh_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_multiple_warehouses_from_user_endpoint(user_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_multiple_warehouses_from_user_payload(*wh_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            (f'Expected status code {HTTPStatus.NOT_FOUND}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_warehouse_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete multiple warehouses from valid user, by user ID.")
    def delete_multiple_warehouses_from_valid_user(self, user_id, list_whs: list):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_multiple_warehouses_from_user_endpoint(user_id),
            headers=self.headers.basic_header(get_token()),
            json=list_whs
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
        logger.warning(f'Successfully delete multiple warehouses qty IDs {len(list_whs)} from user ID {user_id}.')
        return None

    @allure.step("Delete already deleted warehouse from user.(/UserWarehouses)")
    def delete_already_deleted_warehouses_from_users_by_body(self, user_ids: list, warehouse_ids_list: list):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_multiple_warehouses_from_users_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_multiple_warehouses_from_users_payload(user_ids, warehouse_ids_list)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CONFLICT, \
            (f'Expected status code {HTTPStatus.CONFLICT}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_already_done(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete deleted from system warehouse from user.(/UserWarehouses)")
    def delete_deleted_from_system_warehouses_from_users_by_body(self, user_ids: list, warehouse_ids_list: list):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_multiple_warehouses_from_users_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_multiple_warehouses_from_users_payload(user_ids, warehouse_ids_list)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CONFLICT, \
            (f'Expected status code {HTTPStatus.CONFLICT}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_warehouse_deleted(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete valid warehouse from deleted user.(/UserWarehouses)")
    def delete_valid_warehouse_from_deleted_users_by_body(self, user_ids: list, warehouse_ids_list: list):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_multiple_warehouses_from_users_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_multiple_warehouses_from_users_payload(user_ids, warehouse_ids_list)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            (f'Expected status code {HTTPStatus.FORBIDDEN}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_user_deleted(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete valid warehouse from deleted user.(/UserWarehouses)")
    def delete_valid_warehouse_from_deleted_users_by_body(self, user_ids: list, warehouse_ids_list: list):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_multiple_warehouses_from_users_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_multiple_warehouses_from_users_payload(user_ids, warehouse_ids_list)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            (f'Expected status code {HTTPStatus.FORBIDDEN}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_user_deleted(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete valid and deleted from system warehouses from user.(/UserWarehouses)")
    def delete_valid_and_deleted_from_system_warehouses_from_users_by_body(
            self, user_ids: list, warehouse_ids_list: list
    ) -> None:
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_multiple_warehouses_from_users_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_multiple_warehouses_from_users_payload(user_ids, warehouse_ids_list)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CONFLICT, \
            (f'Expected status code {HTTPStatus.CONFLICT}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_warehouse_deleted(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete valid and non-existent warehouses from user.(/UserWarehouses)")
    def delete_valid_and_non_existent_warehouses_from_users_by_body(
            self, user_ids: list, warehouse_ids_list: list
    ) -> None:
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_multiple_warehouses_from_users_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_multiple_warehouses_from_users_payload(user_ids, warehouse_ids_list)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            (f'Expected status code {HTTPStatus.NOT_FOUND}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_warehouse_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete already deleted and non-existent warehouses from user.(/UserWarehouses)")
    def delete_already_deleted_and_non_existent_warehouses_from_users_by_body(
            self, user_ids: list, warehouse_ids_list: list
    ) -> None:
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_multiple_warehouses_from_users_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_multiple_warehouses_from_users_payload(user_ids, warehouse_ids_list)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            (f'Expected status code {HTTPStatus.NOT_FOUND}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_warehouse_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete valid warehouses from valid and deleted from system users.(/UserWarehouses)")
    def delete_valid_warehouses_from_valid_and_deleted_users_by_body(
            self, user_ids: list, warehouse_ids_list: list
    ) -> None:
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_multiple_warehouses_from_users_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_multiple_warehouses_from_users_payload(user_ids, warehouse_ids_list)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            (f'Expected status code {HTTPStatus.FORBIDDEN}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_user_deleted(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete valid warehouses from non-existent and deleted from system users.(/UserWarehouses)")
    def delete_valid_warehouses_from_non_existent_and_deleted_users_by_body(
            self, user_ids: list, warehouse_ids_list: list
    ) -> None:
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_multiple_warehouses_from_users_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_multiple_warehouses_from_users_payload(user_ids, warehouse_ids_list)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            (f'Expected status code {HTTPStatus.FORBIDDEN}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_user_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Get list of unavailable user warehouses.")
    def get_list_of_unavailable_user_warehouses(self, token, user_id):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_user_warehouses_endpoint(user_id),
            headers=self.headers.basic_header(token)
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
        logger.warning(f'Successfully get list of unavailable user warehouses. NO CONTENT.')
        return None

    @allure.step("Get list of non-existent user warehouses.")
    def get_list_of_non_existent_user_warehouses(self, user_id):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_user_warehouses_endpoint(user_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            (f'Expected status code {HTTPStatus.FORBIDDEN}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_user_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Get list of deleted user warehouses.")
    def get_list_of_deleted_user_warehouses(self, user_id):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_user_warehouses_endpoint(user_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            (f'Expected status code {HTTPStatus.FORBIDDEN}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        self.assert_user_deleted(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None
