import random
import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from utils.token_utils import get_token
from services.wh.wh_warehouses.payloads import Payloads
from services.wh.wh_warehouses.endpoints import Endpoints
from config.headers import Headers
from services.wh.wh_warehouses.models.wh_warehouses_model import *
import time
from http import HTTPStatus


class WhWarehousesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Create warehouses.")
    def post_add_warehouses(self):
        erp_name = f"WHErpID {random.randint(1, 999999999)}"
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_warehouses_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_warehouse_payload(
                f"Склад {random.randint(1, 999999999)}",
                erp_name
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
        model = SuccessAddWarehousesModel(result=response.json())
        logger.info(f'Successfully created warehouse with ID:{model.result[0]}.')
        return model, erp_name

    @allure.step("Create two warehouses.")
    def post_add_two_warehouses(self):
        data = {
            "Name": f"Склад {random.randint(1, 99999)}",
            "ErpID": f"WHErpID {random.randint(1, 99999)}",
            "isDefault": False
        }
        data2 = {
            "Name": f"Склад {random.randint(1, 99999)}",
            "ErpID": f"WHErpID {random.randint(1, 99999)}",
            "isDefault": False
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_warehouses_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_warehouse_with_different_fields_payload(data, data2)
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
        model = SuccessAddWarehousesModel(result=response.json())
        logger.info(f'Successfully created two warehouses with IDs:{model.result[0]}, {model.result[1]}.')
        return model

    @allure.step("Create multiple warehouses.")
    def post_add_multiple_warehouses(self, count: int = 300) -> List[int]:
        warehouses_data = []

        for _ in range(count):
            data = {
                "Name": f"Склад {random.randint(99999, 9999999999999999)}",
                "ErpID": f"WHErpID {random.randint(99999, 9999999999999999)}",
                "isDefault": False
            }
            warehouses_data.append(data)

        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_warehouses_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=warehouses_data
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
        model = SuccessAddWarehousesModel(result=response.json())
        logger.info(f'Successfully created 300 warehouses.')
        return model.result

    @allure.step("Create default warehouse.")
    def post_add_default_warehouse(self):
        data = {
            "Name": f"Склад {random.randint(1, 99999999)}",
            "ErpID": f"WHErpID {random.randint(1, 9999999999)}",
            "isDefault": True
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_warehouses_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_warehouse_with_different_fields_payload(data)
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
        model = SuccessAddWarehousesModel(result=response.json())
        logger.info(f'Successfully created default warehouse with ID:{model.result[0]}.')
        return model

    @allure.step("Create two warehouses (one default).")
    def post_add_two_warehouses_default(self):
        data = {
            "Name": f"Склад {random.randint(1, 99999)}",
            "ErpID": f"WHErpID {random.randint(1, 99999)}",
            "isDefault": True
        }
        data2 = {
            "Name": f"Склад {random.randint(1, 99999)}",
            "ErpID": f"WHErpID {random.randint(1, 99999)}",
            "isDefault": False
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_warehouses_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_warehouse_with_different_fields_payload(data, data2)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        model = SuccessAddWarehousesModel(result=response.json())
        assert response.status_code == HTTPStatus.CREATED, f'{response.status_code}, {response.json()}'
        logger.info(f'Successfully created two warehouses one default with ID:{model.result[0]}, {model.result[1]}.')
        return model

    @allure.step("Creating a warehouse with different fields, negative.")
    def post_add_warehouse_parameterized_test(self, data, value_code, value_message, log_info):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_warehouses_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_warehouse_with_different_fields_payload(data)
        )
        end = time.time()
        logger.info(response.headers)
        logger.debug(response.request.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CONFLICT, \
            f'Expected status code {HTTPStatus.CONFLICT}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].code == value_code, "The code does not match the error."
        assert model.list_model[0].message == value_message, "The message does not match the error."
        assert value_code in response.headers["X-Application-Errors"], "Invalid error code in the header"
        logger.error(model.list_model[0].message)
        logger.info(log_info)
        return model

    @allure.step("Delete warehouses by list.")
    def delete_warehouses_by_list(self, *wh_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_warehouses_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_warehouses_by_list(*wh_ids)
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
        logger.warning(f'Successfully delete warehouse with ID:{wh_ids}.')

    @allure.step("Delete list warehouses.")
    def delete_list_warehouses(self, list_whs: list):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_warehouses_endpoint,
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
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.warning(f'Successfully delete list warehouses, qty {len(list_whs)}.')

    @allure.step("Delete warehouses by list (undeleted, deleted).")
    def delete_warehouses_by_list_undeleted_deleted(self, *wh_ids: int):
        """Первый ID не удаленный склад, второй удаленный склад."""
        undeleted_id, deleted_id = wh_ids
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_warehouses_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_warehouses_by_list(*wh_ids)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CONFLICT, \
            f'Expected status code {HTTPStatus.CONFLICT}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].code == "AlreadyDone", \
            f'Expected <AlreadyDone>, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "Операция была выполнена ранее", \
            f'Expected <Операция была выполнена ранее>, but got {model.list_model[0].message}'
        assert "AlreadyDone" in response.headers["X-Application-Errors"], \
            f'Expected <AlreadyDone>, but got {response.headers["X-Application-Errors"]}'
        model_undeleted_wh = self.get_warehouses_by_id(undeleted_id)
        if 'deleted' in model_undeleted_wh.model_fields_set:
            raise AttributeError(f"Warehouse ID {undeleted_id} is deleted.")
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')

    @allure.step("Delete warehouses by list (default, undeleted).")
    def delete_warehouses_by_list_default_undeleted(self, *wh_ids: int):
        """Первый ID склад по умолчанию, второй неудаленный склад."""
        default_id, undeleted_id = wh_ids
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_warehouses_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_warehouses_by_list(*wh_ids)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CONFLICT, \
            f'Expected status code {HTTPStatus.CONFLICT}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].code == "InvalidData", \
            f'Expected <InvalidData>, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "Неверные данные: DefaultWarehouse", \
            f'Expected <Неверные данные: DefaultWarehouse>, but got {model.list_model[0].message}'
        assert "InvalidData" in response.headers["X-Application-Errors"], \
            f'Expected <InvalidData>, but got {response.headers["X-Application-Errors"]}'
        model_default_wh = self.get_warehouses_by_id(default_id)
        if 'deleted' in model_default_wh.model_fields_set:
            raise AttributeError(f"Default warehouse ID {default_id} is deleted.")
        model_undeleted_wh = self.get_warehouses_by_id(undeleted_id)
        if 'deleted' in model_undeleted_wh.model_fields_set:
            raise AttributeError(f"Warehouse ID {undeleted_id} is deleted.")
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')

    @allure.step("Delete warehouses by list (default, deleted).")
    def delete_warehouses_by_list_default_deleted(self, *wh_ids: int):
        """Первый ID склад по умолчанию, второй удаленный склад."""
        default_id, deleted_id = wh_ids
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_warehouses_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_warehouses_by_list(*wh_ids)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CONFLICT, \
            f'Expected status code {HTTPStatus.CONFLICT}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].code == "AlreadyDone", \
            f'Expected <AlreadyDone>, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "Операция была выполнена ранее", \
            f'Expected <Операция была выполнена ранее>, but got {model.list_model[0].message}'
        assert "AlreadyDone" in response.headers["X-Application-Errors"], \
            f'Expected <AlreadyDone>, but got {response.headers["X-Application-Errors"]}'
        model_default_wh = self.get_warehouses_by_id(default_id)
        if 'deleted' in model_default_wh.model_fields_set:
            raise AttributeError(f"Default warehouse ID {default_id} is deleted.")
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')

    @allure.step("Delete warehouses by ID.")
    def delete_warehouse_by_id(self, wh_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_warehouses_by_id_endpoint(wh_id),
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
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.warning(f'Successfully delete warehouse with ID:{wh_id}.')

    @allure.step("Delete default warehouse by ID.")
    def delete_default_warehouse_by_id(self, wh_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_warehouses_by_id_endpoint(wh_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CONFLICT, \
            f'Expected status code {HTTPStatus.CONFLICT}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].code == "InvalidData", \
            f'Expected <InvalidData>, but got {model.list_model[0].code}'
        assert model.list_model[0].message in {"Invalid data: DefaultWarehouse", "Неверные данные: DefaultWarehouse"}, \
            (f'Expected <Invalid data: DefaultWarehouse, Неверные данные: DefaultWarehouse>, '
             f'but got {model.list_model[0].message}')
        assert "InvalidData" in response.headers["X-Application-Errors"], \
            f'Expected <InvalidData>, but got {response.headers["X-Application-Errors"]}'
        model_wh = self.get_warehouses_by_id(wh_id)
        if 'deleted' in model_wh.model_fields_set:
            raise AttributeError("Default warehouse is deleted.")
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')

    @allure.step("Delete deleted warehouse by ID.")
    def delete_deleted_warehouse_by_id(self, wh_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_warehouses_by_id_endpoint(wh_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CONFLICT, \
            f'Expected status code {HTTPStatus.CONFLICT}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].code == "AlreadyDone", \
            f'Expected <AlreadyDone>, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "Операция была выполнена ранее", \
            f'Expected <Операция была выполнена ранее>, but got {model.list_model[0].message}'
        assert "AlreadyDone" in response.headers["X-Application-Errors"], \
            f'Expected <AlreadyDone>, but got {response.headers["X-Application-Errors"]}'
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')

    @allure.step("Get warehouse by ID.")
    def get_warehouses_by_id(self, wh_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_warehouses_by_id_endpoint(wh_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {response.json()}'
        model = WarehousesModel(**response.json())
        logger.info(f'Successfully get warehouse with ID: {wh_id}.')
        return model

    @allure.step("Get warehouse with negative values instead of ID.")
    def get_warehouse_with_negative_values(self, wh_id, status_code):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_warehouses_by_id_endpoint(wh_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response_headers(response.headers)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == status_code, \
            f'Expected status code {status_code}, but got {response.status_code}, {response.json()}'
        assert "ResourceNotFound" in response.headers["X-ServiceFabric"], \
            f"Expected: ResourceNotFound, but got {response.headers["X-ServiceFabric"]}"
        logger.info(f'Expected result: error {status_code}.')
        return None

    @allure.step("Get warehouse a non-existent ID.")
    def get_non_existent_warehouses(self):
        warehouses_list = self.get_list_warehouses_v2()
        if warehouses_list is None:
            non_existent_wh = 1
        else:
            wh_id = int(max(warehouses_list.root.keys(), key=int))
            non_existent_wh = wh_id + 1
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_warehouses_by_id_endpoint(non_existent_wh),
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
            f'Expected status code {HTTPStatus.NO_CONTENT}, but got {response.status_code}, {response.json()}'
        logger.info(f'Successfully get non-existing warehouse.')

    @allure.step("Get list warehouse v2, return non-existent ID.")
    def get_non_existent_warehouse_return_id(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_warehouses_v2_endpoint,
            headers=self.headers.basic_header_with_range(get_token())
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
             f'but got {response.status_code}, {data_response}')
        GetListWarehousesModel(root=response.json())
        qty_items = int(response.headers["Content-Range"].split("/")[-1])
        non_existent_wh = qty_items + 1
        logger.info(f'Successfully get non-existing warehouse ID {non_existent_wh}.')
        return non_existent_wh

    @allure.step("Get list warehouses.")
    def get_list_warehouses(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_warehouses_endpoint,
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
            logger.info('Tenant has no warehouses.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {response.json()}'
        model = GetListWarehousesModel(root=response.json())
        logger.info(f'Successfully get list warehouses.')
        return model

    @allure.step("Head warehouses.")
    def head_warehouses(self):
        model_wh = self.get_list_warehouses_v2()
        start = time.time()
        response = requests.head(
            url=self.endpoints.get_list_warehouses_endpoint,
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
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {response.json()}'
        qty_wh = response.headers["Content-Range"].split("/")[-1]
        qty_wh_get = len(model_wh.root)
        assert int(qty_wh) == qty_wh_get, "Head request returns an incorrect number of warehouses."
        logger.info(f'Successfully get head warehouses. Number of warehouses {qty_wh}, {qty_wh_get}')

    @allure.step("Get list warehouses V2.")
    def get_list_warehouses_v2(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_warehouses_v2_endpoint,
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
            logger.info('Tenant has no warehouses.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {response.json()}'
        model = GetListWarehousesModel(root=response.json())
        logger.info(f'Successfully get list warehouses v2.')
        return model

    @allure.step("Update warehouse.")
    def put_update_warehouse(self, wh_id: int):
        warehouse_before = self.get_warehouses_by_id(wh_id)
        number = random.randint(1, 99999)
        data = {
            "name": f"Измененный склад {number}",
            "erpID": f"Измененный erpID {number}",
            "isDefault": False,
            "id": wh_id
        }
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_warehouses_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_warehouse_payload(data)
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
        warehouse_after = self.get_warehouses_by_id(wh_id)
        assert warehouse_before.name != warehouse_after.name, f"{warehouse_before.name} is equal {warehouse_after.name}"
        assert warehouse_before.erpID != warehouse_after.erpID, \
            f"{warehouse_before.erpID} is equal {warehouse_after.erpID}"
        assert warehouse_after.isDefault is False, \
            f"Expected False, but got {warehouse_after.isDefault}"
        logger.info(f'Successfully update warehouse with ID:{wh_id}.')
        return None

    @allure.step("Update a non-existent warehouse.")
    def put_update_non_existent_warehouse(self) -> None:
        warehouses_list = self.get_list_warehouses_v2()
        if warehouses_list is None:
            non_existent_wh = 1
        else:
            wh_id = int(max(warehouses_list.root.keys(), key=int))
            non_existent_wh = wh_id + 1
        number = random.randint(1, 99999)
        data = {
            "name": f"Измененный склад {number}",
            "erpID": f"Измененный erpID {number}",
            "isDefault": False,
            "id": non_existent_wh
        }
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_warehouses_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_warehouse_payload(data)
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
            f'Expected status code {HTTPStatus.NOT_FOUND}, but got {response.status_code}, {data_response}'
        assert "WarehouseNotFound" in response.headers["X-Application-Errors"], "Invalid error code in the header"
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].code == "WarehouseNotFound", "The code does not match the error."
        assert model.list_model[0].message in {"Warehouse is not found", "Склад не найден"}, \
            "The message does not match the error."
        logger.info(f'Expected result: error 404, message: {model.list_model[0].message}.')
        return None

    @allure.step("Update warehouse without ID field.")
    def put_update_warehouse_without_id_field(self):
        number = random.randint(1, 99999)
        data = {
            "name": f"Измененный склад {number}",
            "erpID": f"Измененный erpID {number}",
            "isDefault": False
        }
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_warehouses_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_warehouse_payload(data)
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
            f'Expected status code {HTTPStatus.CONFLICT}, but got {response.status_code}, {data_response}'
        assert "InvalidData" in response.headers["X-Application-Errors"], "Invalid error code in the header"
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].code == "InvalidData", "The code does not match the error."
        assert model.list_model[0].message == "The field ID must be between 1 and 32767.", \
            "The message does not match the error."
        logger.info(f'Expected result: error 409, message: {model.list_model[0].message}.')
        return None

    @allure.step("Update deleted warehouse.")
    def put_update_deleted_warehouse(self, wh_id):
        number = random.randint(1, 99999)
        data = {
            "name": f"Измененный склад {number}",
            "erpID": f"Измененный erpID {number}",
            "isDefault": False,
            "id": wh_id
        }
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_warehouses_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_warehouse_payload(data)
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
            f'Expected status code {HTTPStatus.CONFLICT}, but got {response.status_code}, {data_response}'
        assert "WarehouseDeleted" in response.headers["X-Application-Errors"], "Invalid error code in the header"
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].code == "WarehouseDeleted", "The code does not match the error."
        assert model.list_model[0].message in {"Warehouse is deleted", "Склад удален"}, \
            "The message does not match the error."
        logger.info(f'Expected result: error 409, message: {model.list_model[0].message}.')
        return None

    @allure.step("PUT restore warehouses by list.")
    def put_restore_warehouses_by_list(self, *wh_ids: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_restore_warehouses_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_restore_warehouses_by_list_payload(*wh_ids)
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
        logger.info(f'Successfully put restore warehouses by list with ID:{wh_ids}.')
        return None

    @allure.step("PUT restore warehouses by list (undeleted, deleted).")
    def put_restore_warehouses_by_list_undeleted_deleted(self, *wh_ids: int):
        """Первый ID неудаленный, второй удаленный."""
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_restore_warehouses_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_restore_warehouses_by_list_payload(*wh_ids)
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
            f'Expected status code {HTTPStatus.CONFLICT}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_already_done(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("PUT restore warehouses by list (undeleted, nonexistent).")
    def put_restore_warehouses_by_list_undeleted_nonexistent(self, undeleted_wh_id: int):
        """Первый ID неудаленный, второй несозданный."""
        warehouses_list = self.get_list_warehouses_v2()
        if warehouses_list is None:
            non_existent_wh = 1
        else:
            wh_id = int(max(warehouses_list.root.keys(), key=int))
            non_existent_wh = wh_id + 1
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_restore_warehouses_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_restore_warehouses_by_list_payload(undeleted_wh_id, non_existent_wh)
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
            f'Expected status code {HTTPStatus.NOT_FOUND}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].code == "WarehouseNotFound", \
            f'Expected <WarehouseNotFound>, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "Склад не найден", \
            f'Expected <Операция была выполнена ранее>, but got {model.list_model[0].message}'
        assert "WarehouseNotFound" in response.headers["X-Application-Errors"], \
            f'Expected <WarehouseNotFound>, but got {response.headers["X-Application-Errors"]}'
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("PUT restore warehouses by list (deleted, nonexistent).")
    def put_restore_warehouses_by_list_deleted_nonexistent(self, deleted_wh_id: int):
        """Первый ID удаленный, второй несозданный."""
        warehouses_list = self.get_list_warehouses_v2()
        if warehouses_list is None:
            non_existent_wh = 1
        else:
            wh_id = int(max(warehouses_list.root.keys(), key=int))
            non_existent_wh = wh_id + 1
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_restore_warehouses_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_restore_warehouses_by_list_payload(deleted_wh_id, non_existent_wh)
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
            f'Expected status code {HTTPStatus.NOT_FOUND}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].code == "WarehouseNotFound", \
            f'Expected <WarehouseNotFound>, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "Склад не найден", \
            f'Expected <Склад не найден>, but got {model.list_model[0].message}'
        assert "WarehouseNotFound" in response.headers["X-Application-Errors"], \
            f'Expected <WarehouseNotFound>, but got {response.headers["X-Application-Errors"]}'
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("PUT restore warehouse by ID.")
    def put_restore_warehouses_by_id(self, wh_id: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_restore_warehouses_by_id_endpoint(wh_id),
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
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.info(f'Successfully put restore warehouse ID:{wh_id}.')
        return None

    @allure.step("PUT restore undeleted warehouse by ID.")
    def put_restore_undeleted_warehouses_by_id(self, wh_id: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_restore_warehouses_by_id_endpoint(wh_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CONFLICT, \
            f'Expected status code {HTTPStatus.CONFLICT}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_already_done(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("PUT restore nonexistent warehouse by ID.")
    def put_restore_nonexistent_warehouses_by_id(self):
        warehouses_list = self.get_list_warehouses_v2()
        if warehouses_list is None:
            non_existent_wh = 1
        else:
            wh_id = int(max(warehouses_list.root.keys(), key=int))
            non_existent_wh = wh_id + 1
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_restore_warehouses_by_id_endpoint(non_existent_wh),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            f'Expected status code {HTTPStatus.NOT_FOUND}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].code == "WarehouseNotFound", \
            f'Expected <WarehouseNotFound>, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "Склад не найден", \
            f'Expected <Склад не найден>, but got {model.list_model[0].message}'
        assert "WarehouseNotFound" in response.headers["X-Application-Errors"], \
            f'Expected <WarehouseNotFound>, but got {response.headers["X-Application-Errors"]}'
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Get list stuff users added to warehouse.")
    def get_list_stuff_users_added_to_warehouse(self, wh_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_users_warehouses_by_wh_id_endpoint(wh_id),
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
            logger.info('Users not added to warehouse.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = UsersWarehousesGetListResponseModel(results=response.json())
        logger.info(f'Successfully get list stuff users added to warehouse.')
        return model

    @allure.step("Add many users to warehouse, by warehouses ID.")
    def post_add_many_users_to_warehouse_by_warehouses_id(self, wh_id: int, *users_ids: int or tuple):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_users_to_warehouse_by_wh_id_endpoint(wh_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_many_users_to_warehouse_by_list(*users_ids)
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
        model = UsersToWarehousesResponseModel(root=response.json())
        logger.info(f'Successfully add many users {users_ids} to warehouse, by warehouses ID:{wh_id}.')
        return model

    @allure.step("Add many users to warehouse, by list ID.")
    def post_add_many_users_to_warehouse_by_list_id(self, wh_id: int, list_users: list):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_users_to_warehouse_by_wh_id_endpoint(wh_id),
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
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = UsersToWarehousesResponseModel(root=response.json())
        logger.info(f'Successfully add many users {list} to warehouse, by warehouses ID:{wh_id}.')
        return model

    @allure.step("Add all stuff users to warehouse, by warehouses ID.")
    def post_add_all_stuff_users_to_warehouse(self, wh_id: int, list_users: list):
        param = {
            "isRelatedToAnyUser": True
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_users_to_warehouse_by_wh_id_endpoint(wh_id), params=param,
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
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = UsersToWarehousesResponseModel(root=response.json())
        missing_ids = [id_ for id_ in list_users if str(id_) not in model.root]
        assert not missing_ids, f"User ID {missing_ids} not added to warehouses {wh_id}"
        logger.info(f'Successfully add all stuff users qty IDs{len(list_users)} to warehouse ID: {wh_id}.')
        return model
