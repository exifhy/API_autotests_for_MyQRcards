import random
import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.wh.wh_receipts.payloads import Payloads
from services.wh.wh_receipts.endpoints import Endpoints
from config.headers import Headers
from services.wh.wh_receipts.models.wh_receipts_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class WhReceiptsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add receipts.")
    def post_add_receipts(self, wh_id: int, erp_name: str):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_receipts_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_receipt_payload(
                wh_id,
                2,
                erp_name,
                str(random.randint(1, 9999999999999999))
            )
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessAddReceiptsModel(result=response.json())
        logger.info(f'Successfully created receipt with ID:{model.result[0]}.')
        return model

    @allure.step("Add three receipts.")
    def post_add_three_receipts(self, wh_id: int, erp_name: str):
        data = {
            "number": str(random.randint(1, 9999999999999999)),
            "warehouseID": wh_id,
            "documentStatusID": 2,
            "erpID": erp_name
        }
        data2 = {
            "number": str(random.randint(1, 9999999999999999)),
            "warehouseID": wh_id,
            "documentStatusID": 2,
            "erpID": erp_name
        }
        data3 = {
            "number": str(random.randint(1, 9999999999999999)),
            "warehouseID": wh_id,
            "documentStatusID": 2,
            "erpID": erp_name
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_receipts_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_receipts_payload(data, data2, data3)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessAddReceiptsModel(result=response.json())
        logger.info(f'Successfully created receipt with ID:{model.result}.')
        return model

    @allure.step("Add two receipts.")
    def post_add_two_receipts(self, wh_id: int, erp_name: str):
        data = {
            "number": str(random.randint(1, 9999999999999999)),
            "warehouseID": wh_id,
            "documentStatusID": 2,
            "erpID": erp_name
        }
        data2 = {
            "number": str(random.randint(1, 9999999999999999)),
            "warehouseID": wh_id,
            "documentStatusID": 2,
            "erpID": erp_name
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_receipts_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_receipts_payload(data, data2)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessAddReceiptsModel(result=response.json())
        logger.info(f'Successfully created receipt with ID:{model.result}.')
        return model

    @allure.step("Add receipt with deleted warehouse.")
    def post_add_receipt_with_deleted_warehouses(self, wh_id: int, erp_name: str):
        data = {
            "number": str(random.randint(1, 9999999999999999)),
            "warehouseID": wh_id,
            "documentStatusID": 2,
            "erpID": erp_name
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_receipts_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_receipts_payload(data)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CONFLICT, \
            f'Expected status code {HTTPStatus.CONFLICT}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].code == "WarehouseDeleted", \
            f'Expected <WarehouseDeleted>, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "Склад удален", \
            f'Expected <Склад удален>, but got {model.list_model[0].message}'
        assert "WarehouseDeleted" in response.headers["X-Application-Errors"], \
            f'Expected <WarehouseDeleted>, but got {response.headers["X-Application-Errors"]}'
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return model

    @allure.step("Add receipt without number field.")
    def post_add_receipt_without_number_field(self, wh_id: int, erp_name: str):
        data = {
            "warehouseID": wh_id,
            "documentStatusID": 2,
            "erpID": erp_name
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_receipts_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_receipts_payload(data)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CONFLICT, \
            f'Expected status code {HTTPStatus.CONFLICT}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return model

    @allure.step("Add receipt without warehouseID field.")
    def post_add_receipt_without_warehouse_id_field(self):
        data = {
            "number": str(random.randint(1, 9999999999999999)),
            "documentStatusID": 2,
            "erpID": "ErpID 1"
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_receipts_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_receipts_payload(data)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CONFLICT, \
            f'Expected status code {HTTPStatus.CONFLICT}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].code == "InvalidData", \
            f'Expected <InvalidData>, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "The field WarehouseID must be between 1 and 32767.", \
            f'Expected <The field WarehouseID must be between 1 and 32767.>, but got {model.list_model[0].message}'
        assert "InvalidData" in response.headers["X-Application-Errors"], \
            f'Expected <InvalidData>, but got {response.headers["X-Application-Errors"]}'
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return model

    @allure.step("Add items receipts.")
    def post_add_items_receipts(self, receipt_id: int, material_id: int):
        qty = random.randint(1, 999)
        unit_id = 166
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_items_receipts_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_items_receipt_payload(
                receipt_id,
                material_id,
                unit_id,
                qty
            )
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.info(f'Successfully add items to receipt with ID:{material_id}.')

    @allure.step("Delete receipts by list.")
    def delete_receipts_by_list(self, *receipt_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_receipts_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_receipts_payload(
                *receipt_ids
            )
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.warning(f'Successfully delete receipts with ID:{receipt_ids}.')

    @allure.step("Delete items receipts by list.")
    def delete_items_receipts_by_list(self, receipt_id: int, *items_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_items_receipts_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_items_receipts_payload(
                receipt_id,
                *items_ids
            )
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.warning(f'Successfully delete items receipts with ID:{items_ids}.')

    @allure.step("Delete item receipt by material ID.")
    def delete_item_receipt_by_material_id(self, receipt_id: int, material_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_receipts_by_receipt_id_material_id_endpoint(
                receipt_id, material_id
            ),
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
            f'Expected status code {HTTPStatus.ACCEPTED}, {response.status_code}, {data_response}'
        logger.warning(f'Successfully delete item receipt ID {receipt_id} by material ID {material_id}.')

    @allure.step("Get receipt by ID.")
    def get_receipt_by_id(self, receipt_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_receipt_by_id_endpoint(receipt_id),
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
        model = ReceiptResultModel(**response.json())
        logger.info(f'Successfully get receipt with ID:{receipt_id}.')
        return model

    @allure.step("Get nonexistent receipt by ID.")
    def get_nonexistent_receipt_by_id(self):
        nonexistent_receipt_id = self.head_qty_receipts() + 1
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_receipt_by_id_endpoint(nonexistent_receipt_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.NO_CONTENT, \
            f'Expected status code {HTTPStatus.NO_CONTENT}, but got {response.status_code}, {data_response}'
        logger.info(f'Successfully get nonexistent receipt with ID:{nonexistent_receipt_id}.')
        return None

    @allure.step("Delete deleted receipt by ID.")
    def delete_deleted_receipt_by_id(self, receipt_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_receipt_by_id_endpoint(receipt_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CONFLICT, \
            f'Expected status code {HTTPStatus.CONFLICT}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_already_done(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete nonexistent receipt by ID.")
    def delete_nonexistent_receipt_by_id(self):
        nonexistent_receipt_id = self.head_qty_receipts() + 1
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_receipt_by_id_endpoint(nonexistent_receipt_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            f'Expected status code {HTTPStatus.NOT_FOUND}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_receipt_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete receipt by ID.")
    def delete_receipt_by_id(self, receipt_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_receipt_by_id_endpoint(receipt_id),
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
        logger.warning(f'Successfully delete receipt with ID:{receipt_id}.')

    @allure.step("Get list receipts.")
    def get_list_receipts(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_receipts_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning("Tenant does not contain receipts")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {(HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)}, '
             f'but got {response.status_code}, {data_response}')
        model = SuccessGetListReceiptResultModel(root=response.json())
        logger.info(f'Successfully get list receipts.')
        return model

    @allure.step("Get list receipts with range.")
    def get_list_receipts_with_range(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_receipts_endpoint,
            headers=self.headers.basic_header_with_range(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning("Tenant does not contain receipts")
            return None
        assert response.status_code in {HTTPStatus.PARTIAL_CONTENT, HTTPStatus.OK}, \
            f'Expected status code {HTTPStatus.PARTIAL_CONTENT, HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessGetListReceiptResultModel(root=response.json())
        qty_items = int(response.headers["Content-Range"].split("/")[-1])
        logger.info(f'Successfully get list receipts with range. Quantity of receipts {len(model.root)}')
        return qty_items

    @allure.step("Head receipts.")
    def head_receipts(self):
        start = time.time()
        response = requests.head(
            url=self.endpoints.head_receipts_endpoint,
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
        qty_receipts = self.get_list_receipts_with_range()
        qty_items = int(response.headers["Content-Range"].split("/")[-1])
        assert qty_items == qty_receipts, \
            f"Expected qty receipts {qty_receipts}, but got {qty_items}"
        logger.info(f'Successfully get head receipts. Quantity of materials {qty_items}.')
        return qty_items

    @allure.step("Check head receipts.")
    def head_qty_receipts(self):
        start = time.time()
        response = requests.head(
            url=self.endpoints.head_receipts_endpoint,
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
        qty_items = int(response.headers["Content-Range"].split("/")[-1])
        logger.info(f'Successfully get head receipts. Quantity of materials {qty_items}.')
        return qty_items

    @allure.step("Update receipt by ID.")
    def put_update_receipts(self, receipt_id: int, wh_id: int, erp_name: str):
        model_before = self.get_receipt_by_id(receipt_id)
        data = {
            "number": str(random.randint(1, 9999999999999999)),
            "warehouseID": wh_id,
            "documentStatusID": 1,
            "erpID": erp_name,
            "id": receipt_id
        }
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_receipts_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_receipts_payload(data)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        model_after = self.get_receipt_by_id(receipt_id)
        assert model_before.number != model_after.number, \
            f"{model_before.number} is equal {model_after.number}, receipt is not updated."
        assert model_before.warehouseID != model_after.warehouseID, \
            f"{model_before.warehouseID} is equal {model_after.warehouseID}, receipt is not updated."
        assert model_before.warehouseName != model_after.warehouseName, \
            f"{model_before.warehouseName} is equal {model_after.warehouseName}, receipt is not updated."
        assert model_before.documentStatusID != model_after.documentStatusID, \
            f"{model_before.documentStatusID} is equal {model_after.documentStatusID}, receipt is not updated."
        assert model_before.erpID != model_after.erpID, \
            f"{model_before.erpID} is equal {model_after.erpID}, receipt is not updated."
        logger.info(f'Successfully update receipt with ID:{receipt_id}.')

    @allure.step("Restore receipts by ID.")
    def put_restore_receipts_by_id(self, receipt_id: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_restore_receipts_by_id_endpoint(receipt_id),
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
        model = self.get_receipt_by_id(receipt_id)
        if 'deleted' in model.model_fields_set:
            raise AttributeError(f"Receipt ID {receipt_id} is deleted.")
        logger.info(f'Successfully restore receipts by ID {receipt_id}.')

    @allure.step("Restore undeleted receipt by ID.")
    def put_restore_undeleted_receipts_by_id(self, receipt_id: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_restore_receipts_by_id_endpoint(receipt_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CONFLICT, \
            f'Expected status code {HTTPStatus.CONFLICT}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_already_done(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Restore nonexistent receipt by ID.")
    def put_restore_nonexistent_receipts_by_id(self):
        nonexistent_receipt_id = self.head_qty_receipts() + 1
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_restore_receipts_by_id_endpoint(nonexistent_receipt_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            f'Expected status code {HTTPStatus.NOT_FOUND}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_receipt_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Restore receipts by list.")
    def put_restore_receipts_by_list(self, *receipts_ids: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_restore_receipts_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_restore_receipts_payload(*receipts_ids)
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
        logger.info(f'Successfully restore receipts by list {receipts_ids}.')
        return None

    @allure.step("Restore receipts by list (undeleted, deleted).")
    def put_restore_undeleted_deleted_receipts_by_list(self, *receipts_ids: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_restore_receipts_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_restore_receipts_payload(*receipts_ids)
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
        self.assert_already_done(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Restore receipts by list (undeleted, undeleted).")
    def put_restore_undeleted_undeleted_receipts_by_list(self, *receipts_ids: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_restore_receipts_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_restore_receipts_payload(*receipts_ids)
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
        self.assert_already_done(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Restore receipts by list (nonexistent, undeleted).")
    def put_restore_nonexistent_undeleted_receipts_by_list(self, receipt_id: int):
        nonexistent_receipt_id = self.head_qty_receipts() + 1
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_restore_receipts_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_restore_receipts_payload(nonexistent_receipt_id, receipt_id)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            f'Expected status code {HTTPStatus.NOT_FOUND}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_receipt_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Restore receipts by list (nonexistent, deleted).")
    def put_restore_nonexistent_deleted_receipts_by_list(self, receipt_id: int):
        nonexistent_receipt_id = self.head_qty_receipts() + 1
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_restore_receipts_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_restore_receipts_payload(nonexistent_receipt_id, receipt_id)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            f'Expected status code {HTTPStatus.NOT_FOUND}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_receipt_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Get list receipt items by receipt ID.")
    def get_list_receipt_items(self, receipt_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_items_receipts_by_id_endpoint(receipt_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning("Tenant does not contain receipt items.")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {(HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)}, '
             f'but got {response.status_code}, {data_response}')
        model = SuccessGetListReceiptItemsModel(results=response.json())
        logger.info(f'Successfully get list receipts items by receipt ID {receipt_id}.')
        return model
