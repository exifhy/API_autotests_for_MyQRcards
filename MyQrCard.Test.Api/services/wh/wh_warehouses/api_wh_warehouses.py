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
        logger.info(f'Successfully created {count} warehouses.')
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
        non_existent_wh = self.get_non_existent_warehouse_return_id()
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

    @allure.step("Verify that Content-Range header equals the total number of warehouses when Fetch = count.")
    def get_list_warehouse_v2_content_range_equals_total_when_fetch_equals_count(self):
        warehouses_plus_one = self.get_non_existent_warehouse_return_id()
        param = {
            "Fetch": warehouses_plus_one - 1,
            "offset": 0
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_warehouses_v2_endpoint, params=param,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.PARTIAL_CONTENT, \
            (f'Expected status code {HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}, {"List warehouses" if response.status_code == 200 else data_response}')
        GetListWarehousesModel(root=response.json())
        assert "Content-Range" in response.headers, \
            f'Expected Content-Range in headers {response.headers}'
        assert f'items=1-{warehouses_plus_one - 1}/{warehouses_plus_one - 1}' == response.headers['Content-Range'], \
            (f'Expected - items=1-{warehouses_plus_one - 1}/{warehouses_plus_one - 1}, '
             f'but got {response.headers["Content-Range"]}')
        logger.info(f'Successfully verify that Content-Range equals the total number of warehouses when Fetch = count.')
        return None

    @allure.step("Verify that Content-Range header is greater than the total number of warehouses when Fetch > count.")
    def get_list_warehouse_v2_content_range_equals_total_when_fetch_greater(self):
        warehouses_plus_one = self.get_non_existent_warehouse_return_id()
        param = {
            "Fetch": warehouses_plus_one,
            "offset": 0
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_warehouses_v2_endpoint, params=param,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.PARTIAL_CONTENT, \
            (f'Expected status code {HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}, {"List warehouses" if response.status_code == 200 else data_response}')
        GetListWarehousesModel(root=response.json())
        assert "Content-Range" in response.headers, \
            f'Expected Content-Range in headers {response.headers}'
        assert f'items=1-{warehouses_plus_one}/{warehouses_plus_one - 1}' == response.headers['Content-Range'], \
            (f'Expected - items=1-{warehouses_plus_one}/{warehouses_plus_one - 1}, '
             f'but got {response.headers["Content-Range"]}')
        logger.info(f'Successfully verify Content-Range is greater than total number of warehouses when Fetch > count.')
        return None

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
        non_existent_wh = self.get_non_existent_warehouse_return_id()
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
        qty_wh_get = non_existent_wh - 1
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
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}, {response.json()}')
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
        non_existent_wh = self.get_non_existent_warehouse_return_id()
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
        non_existent_wh = self.get_non_existent_warehouse_return_id()
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
        non_existent_wh = self.get_non_existent_warehouse_return_id()
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
        non_existent_wh = self.get_non_existent_warehouse_return_id()
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

    @allure.step("Get checking that no users have been added to the warehouse.")
    def get_no_users_added_to_warehouse(self, wh_id: int):
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
        assert response.status_code == HTTPStatus.NO_CONTENT, \
            f'Expected status code {HTTPStatus.NO_CONTENT}, but got {response.status_code}, {data_response}'
        logger.info(f'Successfully get no users have been added to the warehouse.')
        return None

    @allure.step("Get list of users of the non-existent warehouse.")
    def get_list_users_of_non_existent_warehouse(self, wh_id: int):
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
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            f'Expected status code {HTTPStatus.NOT_FOUND}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_warehouse_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

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

    @allure.step("Add valid user to deleted from sys warehouse, by warehouse ID.")
    def post_add_user_to_deleted_warehouse_by_wh_id(self, wh_id: int, *users_ids: int or tuple):
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
        assert response.status_code == HTTPStatus.CONFLICT, \
            f'Expected status code {HTTPStatus.CONFLICT}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_warehouse_deleted(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add deleted from sys user to valid warehouse, by warehouse ID.")
    def post_add_deleted_user_to_valid_warehouse_by_wh_id(self, wh_id: int, *users_ids: int or tuple):
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
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            f'Expected status code {HTTPStatus.FORBIDDEN}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_user_deleted(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add deleted and valid users to valid warehouse, by warehouse ID.")
    def post_add_deleted_and_valid_user_to_warehouse_by_wh_id(self, wh_id: int, *users_ids: int or tuple):
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
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            f'Expected status code {HTTPStatus.FORBIDDEN}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_user_deleted(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add deleted and non-existent users to valid warehouse, by warehouse ID.")
    def post_add_deleted_and_non_existent_user_to_warehouse_by_wh_id(self, wh_id: int, *users_ids: int or tuple):
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
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            f'Expected status code {HTTPStatus.FORBIDDEN}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_user_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add valid, deleted and non-existent users to valid warehouse, by warehouse ID.")
    def post_add_valid_deleted_and_non_existent_user_to_warehouse_by_wh_id(self, wh_id: int, *users_ids: int or tuple):
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
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            f'Expected status code {HTTPStatus.FORBIDDEN}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_user_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add empty list to valid warehouse, by warehouse ID.")
    def post_add_empty_list_to_warehouse_by_wh_id(self, wh_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_users_to_warehouse_by_wh_id_endpoint(wh_id),
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
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            f'Expected status code {HTTPStatus.FORBIDDEN}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_user_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add empty list to valid warehouse, by warehouse ID.")
    def post_add_empty_list_to_warehouse_by_wh_id(self, wh_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_users_to_warehouse_by_wh_id_endpoint(wh_id),
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
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            f'Expected status code {HTTPStatus.FORBIDDEN}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_user_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add null to valid warehouse, by warehouse ID.")
    def post_add_null_to_warehouse_by_wh_id(self, wh_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_users_to_warehouse_by_wh_id_endpoint(wh_id),
            headers=self.headers.basic_header(get_token()),
            json=None
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR, \
            f'Expected status code {HTTPStatus.INTERNAL_SERVER_ERROR}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].message == "Value cannot be null. (Parameter 'source')", \
            f"Expected <Value cannot be null. (Parameter 'source')>, but got <{model.list_model[0].message}>"
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add valid, abc, null to valid warehouse, by warehouse ID.")
    def post_add_valid_abc_null_to_warehouse_by_wh_id(self, wh_id: int, *users_ids: int or tuple):
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
        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR, \
            f'Expected status code {HTTPStatus.INTERNAL_SERVER_ERROR}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].message == "Value cannot be null. (Parameter 'source')", \
            f"Expected <Value cannot be null. (Parameter 'source')>, but got <{model.list_model[0].message}>"
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add valid user to already added warehouse, by warehouse ID.")
    def post_add_valid_user_to_already_added_warehouse_by_wh_id(self, wh_id: int, *users_ids: int or tuple):
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
        assert response.status_code == HTTPStatus.CONFLICT, \
            f'Expected status code {HTTPStatus.CONFLICT}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_already_done(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add valid user to unavailable warehouse, by warehouse ID.")
    def post_add_valid_user_to_unavailable_warehouse_by_wh_id(self, token, wh_id: int, *users_ids: int or tuple):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_users_to_warehouse_by_wh_id_endpoint(wh_id),
            headers=self.headers.basic_header(token),
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
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            f'Expected status code {HTTPStatus.FORBIDDEN}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].code == "AccessDenied", \
            f'Expected <AccessDenied>, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "Доступ запрещён: Указанный склад", \
            f'Expected <Доступ запрещён: Указанный склад>, but got {model.list_model[0].message}'
        assert "AccessDenied" in response.headers["X-Application-Errors"], \
            f'Expected <AccessDenied>, but got {response.headers["X-Application-Errors"]}'
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add unavailable user to valid warehouse, by warehouse ID.")
    def post_add_unavailable_user_to_valid_warehouse_by_wh_id(self, token, wh_id: int, *users_ids: int or tuple):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_users_to_warehouse_by_wh_id_endpoint(wh_id),
            headers=self.headers.basic_header(token),
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
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            f'Expected status code {HTTPStatus.FORBIDDEN}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].code == "AccessDenied", \
            f'Expected <AccessDenied>, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "Доступ запрещён: Обрабатываемый пользователь", \
            f'Expected <Доступ запрещён: Обрабатываемый пользователь>, but got {model.list_model[0].message}'
        assert "AccessDenied" in response.headers["X-Application-Errors"], \
            f'Expected <AccessDenied>, but got {response.headers["X-Application-Errors"]}'
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add valid user to non-existent warehouse, by warehouse ID.")
    def post_add_valid_user_to_non_existent_warehouse_by_wh_id(self, wh_id: int, *users_ids: int or tuple):
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
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            f'Expected status code {HTTPStatus.NOT_FOUND}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_warehouse_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add non-existent user to valid warehouse, by warehouse ID.")
    def post_add_non_existent_user_to_valid_warehouse_by_wh_id(self, wh_id: int, *users_ids: int or tuple):
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
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            f'Expected status code {HTTPStatus.FORBIDDEN}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_user_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add valid user to valid warehouse, without token.")
    def post_add_user_to_warehouse_without_token(self, wh_id: int, *users_ids: int or tuple):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_users_to_warehouse_by_wh_id_endpoint(wh_id),
            headers=self.headers.basic_header_without_authorization,
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
        assert response.status_code == HTTPStatus.UNAUTHORIZED, \
            f'Expected status code {HTTPStatus.UNAUTHORIZED}, but got {response.status_code}, {data_response}'
        logger.warning(f'Expected result: error {response.status_code}.')
        return None

    @allure.step("Add valid user to valid warehouse, without token, Warehouses/users.")
    def post_add_user_to_warehouse_without_token_by_list(self, list_wh: list, list_users_ids: list):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_users_to_warehouses_by_list_endpoint,
            headers=self.headers.basic_header_without_authorization,
            json=self.payloads.post_add_multiple_users_to_warehouses_payload(list_wh, list_users_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, \
            f'Expected status code {HTTPStatus.UNAUTHORIZED}, but got {response.status_code}, {data_response}'
        logger.warning(f'Expected result: error {response.status_code}.')
        return None

    @allure.step("Add valid users to valid warehouse, Warehouses/users.")
    def post_add_valid_users_to_valid_warehouse_by_list(self, list_wh: list, list_users_ids: list):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_users_to_warehouses_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_users_to_warehouses_payload(list_wh, list_users_ids)
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
        logger.info(f'Successfully add users qty {len(list_users_ids)} to warehouses qty IDs {len(list_wh)}.')
        return model

    @allure.step("Add valid users to deleted from sys warehouse, Warehouses/users.")
    def post_add_valid_users_to_deleted_warehouse_by_list(self, list_wh: list, list_users_ids: list):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_users_to_warehouses_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_users_to_warehouses_payload(list_wh, list_users_ids)
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
        self.assert_warehouse_deleted(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add all users to valid warehouse, Warehouses/users.")
    def post_add_all_users_to_warehouse_by_list(self, wh_id: int, list_users_ids: list):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_users_to_warehouses_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_all_users_to_warehouse_by_list_payload(wh_id)
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
        missing_ids = [id_ for id_ in list_users_ids if str(id_) not in model.root]
        assert not missing_ids, f"User ID {missing_ids} not added to warehouses {wh_id}"
        logger.info(f'Successfully add all users qty IDs {len(list_users_ids)} to warehouse {wh_id} by list.')
        return model

    @allure.step("Add all users with user ID to valid warehouse, Warehouses/users.")
    def post_add_all_users_with_user_id_to_warehouse_by_list(self, wh_id: int, list_users_ids: list):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_users_to_warehouses_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_all_users_with_user_id_to_warehouse_by_list_payload(wh_id, list_users_ids[0])
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
        missing_ids = [id_ for id_ in list_users_ids if str(id_) not in model.root]
        assert not missing_ids, f"User ID {missing_ids} not added to warehouses {wh_id}"
        logger.info(f'Successfully add all users qty IDs {len(list_users_ids)} to warehouse {wh_id} by list.')
        return model

    @allure.step("Add deleted users to vali warehouse, Warehouses/users.")
    def post_add_deleted_user_to_valid_warehouse_by_list(self, list_wh: list, list_users_ids: list):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_users_to_warehouses_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_users_to_warehouses_payload(list_wh, list_users_ids)
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
            f'Expected status code {HTTPStatus.FORBIDDEN}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_user_deleted(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add valid user to non-existent warehouse, Warehouses/users.")
    def post_add_user_to_non_existent_warehouse_by_list(self, list_wh: list, list_users_ids: list):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_users_to_warehouses_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_users_to_warehouses_payload(list_wh, list_users_ids)
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
        self.assert_warehouse_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add non-existent user to valid warehouse, Warehouses/users.")
    def post_add_non_existent_user_to_valid_warehouse_by_list(self, list_wh: list, list_users_ids: list):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_users_to_warehouses_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_users_to_warehouses_payload(list_wh, list_users_ids)
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
            f'Expected status code {HTTPStatus.FORBIDDEN}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_user_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add valid and deleted from sys user to valid warehouse, Warehouses/users.")
    def post_add_valid_and_deleted_user_to_valid_warehouse_by_list(self, list_wh: list, list_users_ids: list):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_users_to_warehouses_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_users_to_warehouses_payload(list_wh, list_users_ids)
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
            f'Expected status code {HTTPStatus.FORBIDDEN}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_user_deleted(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add valid and non-existent user to valid warehouse, Warehouses/users.")
    def post_add_valid_and_non_existent_user_to_valid_warehouse_by_list(self, list_wh: list, list_users_ids: list):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_users_to_warehouses_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_users_to_warehouses_payload(list_wh, list_users_ids)
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
            f'Expected status code {HTTPStatus.FORBIDDEN}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_user_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add valid user to valid and deleted warehouses, Warehouses/users.")
    def post_add_valid_user_to_valid_and_deleted_warehouses_by_list(self, list_wh: list, list_users_ids: list):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_users_to_warehouses_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_users_to_warehouses_payload(list_wh, list_users_ids)
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
        self.assert_warehouse_deleted(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add valid user to valid and non-existent warehouses, Warehouses/users.")
    def post_add_valid_user_to_valid_and_non_existent_warehouses_by_list(self, list_wh: list, list_users_ids: list):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_users_to_warehouses_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_users_to_warehouses_payload(list_wh, list_users_ids)
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
        self.assert_warehouse_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add valid and non-existent, deleted users to warehouses, Warehouses/users.")
    def post_add_valid_non_existent_deleted_users_to_warehouses_by_list(self, list_wh: list, list_users_ids: list):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_users_to_warehouses_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_users_to_warehouses_payload(list_wh, list_users_ids)
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
            f'Expected status code {HTTPStatus.FORBIDDEN}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_user_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add valid user to null warehouse, Warehouses/users.")
    def post_add_valid_user_to_warehouse_null_by_list(self, list_wh: list, list_users_ids: list):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_users_to_warehouses_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_users_to_warehouses_payload(list_wh, list_users_ids)
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
        assert model.list_model[0].code == "ParameterOutOfRange", \
            f'Expected <ParameterOutOfRange>, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "Значение параметра [WarehouseID] находится вне допустимого диапазона.", \
            (f'Expected <Значение параметра [WarehouseID] находится вне допустимого диапазона.>, '
             f'but got {model.list_model[0].message}')
        assert "ParameterOutOfRange" in response.headers["X-Application-Errors"], \
            f'Expected <ParameterOutOfRange>, but got {response.headers["X-Application-Errors"]}'
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add empty list users to valid warehouse, Warehouses/users.")
    def post_add_empty_list_users_to_warehouse_by_list(self, wh_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_users_to_warehouses_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_empty_list_users_to_warehouse_by_list_payload(wh_id)
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
            f'Expected status code {HTTPStatus.FORBIDDEN}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_user_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add null users to valid warehouse, Warehouses/users.")
    def post_add_null_user_to_warehouse_by_list(self, wh_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_users_to_warehouses_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_null_user_to_warehouse_by_list_payload(wh_id)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR, \
            f'Expected status code {HTTPStatus.INTERNAL_SERVER_ERROR}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].message == "Value cannot be null. (Parameter 'source')", \
            f"Expected <Value cannot be null. (Parameter 'source')>, but got {model.list_model[0].message}"
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add valid user to already added warehouse, Warehouses/users.")
    def post_add_user_to_already_added_warehouse_by_list(self, list_wh: list, list_users_ids: list):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_users_to_warehouses_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_multiple_users_to_warehouses_payload(list_wh, list_users_ids)
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

    @allure.step("Add valid user to unavailable warehouse, Warehouses/users.")
    def post_add_user_to_unavailable_warehouse_by_list(self, token, list_wh: list, list_users_ids: list):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_users_to_warehouses_by_list_endpoint,
            headers=self.headers.basic_header(token),
            json=self.payloads.post_add_multiple_users_to_warehouses_payload(list_wh, list_users_ids)
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
            f'Expected status code {HTTPStatus.FORBIDDEN}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].code == "AccessDenied", \
            f'Expected <AccessDenied>, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "Доступ запрещён: Указанный склад", \
            f'Expected <Доступ запрещён: Указанный склад>, but got {model.list_model[0].message}'
        assert "AccessDenied" in response.headers["X-Application-Errors"], \
            f'Expected <AccessDenied>, but got {response.headers["X-Application-Errors"]}'
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Add unavailable user to valid warehouse, Warehouses/users.")
    def post_add_unavailable_user_to_valid_warehouse_by_list(self, token, list_wh: list, list_users_ids: list):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_users_to_warehouses_by_list_endpoint,
            headers=self.headers.basic_header(token),
            json=self.payloads.post_add_multiple_users_to_warehouses_payload(list_wh, list_users_ids)
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
            f'Expected status code {HTTPStatus.FORBIDDEN}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].code == "AccessDenied", \
            f'Expected <AccessDenied>, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "Доступ запрещён: Обрабатываемый пользователь", \
            f'Expected <Доступ запрещён: Обрабатываемый пользователь>, but got {model.list_model[0].message}'
        assert "AccessDenied" in response.headers["X-Application-Errors"], \
            f'Expected <AccessDenied>, but got {response.headers["X-Application-Errors"]}'
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete user from warehouse by warehouse ID.")
    def delete_users_from_warehouse_by_wh_id(self, wh_id: int, *user_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_users_from_warehouse_by_wh_id_endpoint(wh_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_list_users_from_warehouse_by_id_payload(*user_ids)
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
        logger.warning(f'Successfully delete user ID {user_ids} from warehouse with ID: {wh_id}.')

    @allure.step("Delete list users from warehouse by warehouse ID.")
    def delete_list_users_from_warehouse_by_wh_id(self, wh_id: int, list_users: list):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_users_from_warehouse_by_wh_id_endpoint(wh_id),
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
        logger.warning(f'Successfully delete users qty IDs {len(list_users)} from warehouse with ID:{wh_id}.')

    @allure.step("Delete user from already deleted warehouse by warehouse ID.")
    def delete_users_from_already_deleted_warehouse_by_wh_id(self, wh_id: int, *user_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_users_from_warehouse_by_wh_id_endpoint(wh_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_list_users_from_warehouse_by_id_payload(*user_ids)
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

    @allure.step("Delete user from non-existent warehouse by warehouse ID.")
    def delete_user_from_non_existent_warehouse_by_wh_id(self, wh_id: int, *user_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_users_from_warehouse_by_wh_id_endpoint(wh_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_list_users_from_warehouse_by_id_payload(*user_ids)
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
        self.assert_warehouse_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete non-existent user from warehouse by warehouse ID.")
    def delete_non_existent_user_from_valid_warehouse_by_wh_id(self, wh_id: int, *user_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_users_from_warehouse_by_wh_id_endpoint(wh_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_list_users_from_warehouse_by_id_payload(*user_ids)
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
            f'Expected status code {HTTPStatus.FORBIDDEN}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_user_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete valid, deleted, non-existent users from warehouse by warehouse ID.")
    def delete_valid_non_existent_deleted_user_from_warehouse_by_wh_id(self, wh_id: int, *user_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_users_from_warehouse_by_wh_id_endpoint(wh_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_list_users_from_warehouse_by_id_payload(*user_ids)
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
            f'Expected status code {HTTPStatus.FORBIDDEN}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_user_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete empty list users from valid warehouse by warehouse ID.")
    def delete_empty_list_users_from_warehouse_by_wh_id(self, wh_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_users_from_warehouse_by_wh_id_endpoint(wh_id),
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
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            f'Expected status code {HTTPStatus.FORBIDDEN}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_user_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete users=null from valid warehouse by warehouse ID.")
    def delete_null_from_warehouse_by_wh_id(self, wh_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_users_from_warehouse_by_wh_id_endpoint(wh_id),
            headers=self.headers.basic_header(get_token()),
            json=None
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR, \
            f'Expected status code {HTTPStatus.INTERNAL_SERVER_ERROR}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].message == "Value cannot be null. (Parameter 'source')", \
            f"Expected <Value cannot be null. (Parameter 'source')>, but got {model.list_model[0].message}"
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete valid user from deleted from sys warehouse by warehouse ID.")
    def delete_valid_user_from_deleted_from_sys_warehouse_by_wh_id(self, wh_id: int, *user_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_users_from_warehouse_by_wh_id_endpoint(wh_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_list_users_from_warehouse_by_id_payload(*user_ids)
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
        self.assert_warehouse_deleted(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete deleted from sys user from valid warehouse by warehouse ID.")
    def delete_deleted_user_from_valid_warehouse_by_wh_id(self, wh_id: int, *user_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_users_from_warehouse_by_wh_id_endpoint(wh_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_list_users_from_warehouse_by_id_payload(*user_ids)
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
            f'Expected status code {HTTPStatus.FORBIDDEN}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_user_deleted(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete all users from valid warehouse by warehouse ID. isRelatedToAnyUser=true")
    def delete_all_users_from_valid_warehouse_by_wh_id(self, wh_id: int, *user_ids: int or tuple):
        param = {
            "isRelatedToAnyUser": True
        }
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_users_from_warehouse_by_wh_id_endpoint(wh_id), params=param,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_list_users_from_warehouse_by_id_payload(*user_ids)
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
        self.get_no_users_added_to_warehouse(wh_id)
        logger.warning(f'Successfully delete all users from warehouse with ID:{wh_id}.')
        return None

    @allure.step("Delete valid user from valid warehouse by warehouse ID, without authorization.")
    def delete_users_from_warehouse_without_authorization(self, wh_id: int, *user_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_users_from_warehouse_by_wh_id_endpoint(wh_id),
            headers=self.headers.basic_header_without_authorization,
            json=self.payloads.delete_list_users_from_warehouse_by_id_payload(*user_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, \
            f'Expected status code {HTTPStatus.UNAUTHORIZED}, but got {response.status_code}, {data_response}'
        logger.warning(f'Expected result: error {response.status_code}, message: UNAUTHORIZED.')
        return None

    @allure.step("Delete valid user from valid warehouse, Warehouses/users, without authorization.")
    def delete_users_from_warehouse_by_list_without_authorization(self, wh_id: int, *user_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_users_from_warehouses_by_list_endpoint,
            headers=self.headers.basic_header_without_authorization,
            json=self.payloads.delete_all_users_from_warehouses_payload(wh_id, *user_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, \
            f'Expected status code {HTTPStatus.UNAUTHORIZED}, but got {response.status_code}, {data_response}'
        logger.warning(f'Expected result: error {response.status_code}, message: UNAUTHORIZED.')
        return None

    @allure.step("Delete all users from valid warehouse, Warehouses/users. isRelatedToAnyUser=true.")
    def delete_all_users_from_valid_warehouse_by_list(self, wh_id: int, *user_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_users_from_warehouses_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_all_users_from_warehouses_payload(wh_id, *user_ids)
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
        self.get_no_users_added_to_warehouse(wh_id)
        logger.warning(f'Successfully delete all users from warehouse with ID:{wh_id}. Warehouses/users.')
        return None

    @allure.step("Delete valid users from valid warehouse, Warehouses/users.")
    def delete_users_from_valid_warehouses_by_list(self, list_wh: list, list_users: list):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_users_from_warehouses_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_multiple_users_from_warehouses_payload(list_wh, list_users)
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
        logger.warning(f'Successfully delete users qty {len(list_users)} from warehouse '
                       f'qty {len(list_wh)}. Warehouses/users.')
        return None

    @allure.step("Delete valid user from already deleted warehouse, Warehouses/users.")
    def delete_users_from_already_deleted_warehouse_by_list(self, list_wh: list, list_users: list):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_users_from_warehouses_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_multiple_users_from_warehouses_payload(list_wh, list_users)
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
        logger.warning(f'Expected result: error {response.status_code}, message: UNAUTHORIZED.')
        return None

    @allure.step("Delete valid user from non-existent warehouse, Warehouses/users.")
    def delete_users_from_non_existent_warehouse_by_list(self, list_wh: list, list_users: list):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_users_from_warehouses_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_multiple_users_from_warehouses_payload(list_wh, list_users)
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
        self.assert_warehouse_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete non-existent user from warehouse, Warehouses/users.")
    def delete_non_existent_users_from_warehouse_by_list(self, list_wh: list, list_users: list):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_users_from_warehouses_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_multiple_users_from_warehouses_payload(list_wh, list_users)
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
            f'Expected status code {HTTPStatus.FORBIDDEN}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_user_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete valid, deleted, non-existent users from warehouse, Warehouses/users.")
    def delete_valid_non_existent_deleted_users_from_warehouse_by_list(self, list_wh: list, list_users: list):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_users_from_warehouses_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_multiple_users_from_warehouses_payload(list_wh, list_users)
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
            f'Expected status code {HTTPStatus.FORBIDDEN}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_user_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete deleted, non-existent users from deleted warehouse, Warehouses/users.")
    def delete_non_existent_deleted_users_from_deleted_warehouse_by_list(self, list_wh: list, list_users: list):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_users_from_warehouses_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_multiple_users_from_warehouses_payload(list_wh, list_users)
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
        self.assert_warehouse_deleted(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete (deleted, non-existent), (valid) users from valid warehouses. Warehouses/users.")
    def delete_non_existent_deleted_and_valid_users_from_warehouses_by_list(self, list_wh: list, list_users: list):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_users_from_warehouses_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_multiple_users_from_warehouses_payload(list_wh, list_users)
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
            f'Expected status code {HTTPStatus.FORBIDDEN}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_user_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete valid user from deleted from sys warehouse. Warehouses/users.")
    def delete_valid_users_from_deleted_from_sys_warehouse_by_list(self, list_wh: list, list_users: list):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_users_from_warehouses_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_multiple_users_from_warehouses_payload(list_wh, list_users)
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
        self.assert_warehouse_deleted(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete deleted from sys user from valid warehouse. Warehouses/users.")
    def delete_deleted_from_sys_user_from_valid_warehouse_by_list(self, list_wh: list, list_users: list):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_users_from_warehouses_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_multiple_users_from_warehouses_payload(list_wh, list_users)
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
            f'Expected status code {HTTPStatus.FORBIDDEN}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_user_deleted(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete valid user from warehouse=null. Warehouses/users.")
    def delete_valid_user_from_warehouse_null_by_list(self, user_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_users_from_warehouses_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_valid_users_from_warehouse_null_by_list_payload(user_id)
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
        assert model.list_model[0].code == "ParameterOutOfRange", \
            f'Expected <ParameterOutOfRange>, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "Значение параметра [WarehouseID] находится вне допустимого диапазона.", \
            (f'Expected <Значение параметра [WarehouseID] находится вне допустимого диапазона.>, '
             f'but got {model.list_model[0].message}')
        assert "ParameterOutOfRange" in response.headers["X-Application-Errors"], \
            f'Expected <ParameterOutOfRange>, but got {response.headers["X-Application-Errors"]}'
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete empty list users from valid warehouse. Warehouses/users.")
    def delete_empty_list_users_from_valid_warehouse_by_list(self, wh_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_users_from_warehouses_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_empty_list_users_from_valid_warehouse_by_list_payload(wh_id)
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
            f'Expected status code {HTTPStatus.FORBIDDEN}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_user_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete user=null from valid warehouse. Warehouses/users.")
    def delete_user_is_null_from_valid_warehouse_by_list(self, wh_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_users_from_warehouses_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_user_null_from_valid_warehouse_by_list_payload(wh_id)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR, \
            f'Expected status code {HTTPStatus.INTERNAL_SERVER_ERROR}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].message == "Value cannot be null. (Parameter 'source')", \
            f"Expected <Value cannot be null. (Parameter 'source')>, but got {model.list_model[0].message}"
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None
