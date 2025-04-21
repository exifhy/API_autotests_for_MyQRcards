import base64
import io
import random
import allure
import requests
from PIL import Image
from loguru import logger
from requests import JSONDecodeError
from requests_toolbelt import MultipartEncoder
from utils.helper import Helper
from services.wh.wh_materials.payloads import Payloads
from services.wh.wh_materials.endpoints import Endpoints
from config.headers import Headers
from services.wh.wh_materials.models.wh_materials_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class WhMaterialsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Create material.")
    def post_add_materials(self):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_materials_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_materials_payload(
                f"Материал {random.randint(1, 99999)}",
                currency_id=1,
                unit_id=166,
                erp_name=f"MErpID {random.randint(1, 99999)}"
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
        model = SuccessAddMaterialsModel(result=response.json())
        logger.info(f'Successfully created material with ID:{model.result[0]}.')
        return model

    @allure.step("Create of three materials.")
    def post_add_three_materials(self):
        data = {
            "name": f"Материал {random.randint(1, 99999)}",
            "erpID": f"MErpID {random.randint(1, 99999)}",
            "measurementUnitID": 166,
            "Cost": 10.50,
            "costCurrencyID": 1,
            "PurchaseCost": 10.50,
            "purchaseCostCurrencyID": 1,
        }
        data2 = {
            "name": f"Материал {random.randint(1, 99999)}",
            "erpID": f"MErpID {random.randint(1, 99999)}",
            "measurementUnitID": 166,
            "Cost": 10.50,
            "costCurrencyID": 1,
            "PurchaseCost": 10.50,
            "purchaseCostCurrencyID": 1,
        }
        data3 = {
            "name": f"Материал {random.randint(1, 99999)}",
            "erpID": f"MErpID {random.randint(1, 99999)}",
            "measurementUnitID": 166,
            "Cost": 10.50,
            "costCurrencyID": 1,
            "PurchaseCost": 10.50,
            "purchaseCostCurrencyID": 1,
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_materials_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_three_materials_payload(data, data2, data3)
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
        model = SuccessAddMaterialsModel(result=response.json())
        logger.info(f'Successfully created material with ID:{model.result[0]}.')
        return model

    @allure.step("Create of two materials.")
    def post_add_two_materials(self):
        data = {
            "name": f"Материал {random.randint(1, 99999)}",
            "erpID": f"MErpID {random.randint(1, 99999)}",
            "measurementUnitID": 166,
            "Cost": 10.50,
            "costCurrencyID": 1,
            "PurchaseCost": 10.50,
            "purchaseCostCurrencyID": 1,
        }
        data2 = {
            "name": f"Материал {random.randint(1, 99999)}",
            "erpID": f"MErpID {random.randint(1, 99999)}",
            "measurementUnitID": 166,
            "Cost": 10.50,
            "costCurrencyID": 1,
            "PurchaseCost": 10.50,
            "purchaseCostCurrencyID": 1,
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_materials_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_three_materials_payload(data, data2)
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
        model = SuccessAddMaterialsModel(result=response.json())
        logger.info(f'Successfully created material with ID:{model.result[0]}.')
        return model

    @allure.step("Delete materials by list.")
    def delete_materials_by_list(self, *materials_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_materials_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_materials_by_list(*materials_ids)
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
        logger.warning(f'Successfully delete materials with ID:{materials_ids}.')

    @allure.step("Delete materials by list negative <already done>.")
    def delete_materials_by_list_negative_already_done(self, *materials_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_materials_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_materials_by_list(*materials_ids)
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
        return None

    @allure.step("Delete materials by list negative <not found>.")
    def delete_materials_by_list_negative_not_found(self, material_id: int):
        qty_materials = self.get_list_materials_v2_content_range()
        nonexistent_material = qty_materials + 1
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_materials_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_materials_by_list(nonexistent_material, material_id)
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
        assert model.list_model[0].code == "MaterialNotFound", \
            f'Expected <MaterialNotFound>, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "Номенклатура не найдена", \
            f'Expected <Номенклатура не найдена>, but got {model.list_model[0].message}'
        assert "MaterialNotFound" in response.headers["X-Application-Errors"], \
            f'Expected <MaterialNotFound>, but got {response.headers["X-Application-Errors"]}'
        assert "ResourceNotFound" in response.headers["X-ServiceFabric"], \
            f'Expected <ResourceNotFound>, but got {response.headers["X-ServiceFabric"]}'
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Get material by ID.")
    def get_material_by_id(self, materials_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_materials_by_id_endpoint(materials_id),
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
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = MaterialModel(**response.json())
        logger.info(f'Successfully get material with Id: {materials_id}.')
        return model

    @allure.step("Get list attachments by material ID.")
    def get_list_attachments_by_material_id(self, material_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_materials_attachments_by_material_id_endpoint(material_id),
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
            logger.warning("Materials has no attachments.")
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessGetListMaterialAttachmentListResultModel(root=response.json())
        logger.info(f'Successfully get list attachments by material ID {material_id}.')
        return model

    @allure.step("Add attachments to material by list.")
    def post_attachments_to_material_by_list(self, material_id: int, *attachments_ids: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_bind_materials_attachments_by_id_endpoint(material_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_attachments_to_material_by_list_payload(*attachments_ids)
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
        model = SuccessAddMaterialAttachmentPostResultModel(results=response.json())
        logger.info(f'Successfully add attachments {attachments_ids} to material by ID {material_id}.')
        return model

    @allure.step("Delete attachments from material by list.")
    def delete_attachments_from_material_by_list(self, material_id: int, *attachments_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_materials_attachments_by_list_endpoint(material_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_attachments_from_material_by_list_payload(*attachments_ids)
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
        logger.warning(f'Successfully delete attachments {attachments_ids} from material by ID {material_id}.')

    @allure.step("Get attachment from material by ID.")
    def get_attachment_from_material_by_id(self, material_id: int, attachment_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_material_attachment_by_id_endpoint(material_id, attachment_id),
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
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = MaterialAttachmentResultModel(**response.json())
        logger.info(f'Successfully get attachment ID {attachment_id} from material by ID {material_id}.')
        return model

    @allure.step("Delete attachment by ID from material by ID.")
    def delete_attachment_from_material_by_id(self, material_id: int, attachments_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_material_attachment_by_id_endpoint(material_id, attachments_id),
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
        logger.warning(f'Successfully delete attachment ID {attachments_id} from material by ID {material_id}.')

    @allure.step("Get TemporaryRedirect to a temporary link for downloading the attachment file from material.")
    def get_downloading_attachment_file_from_material(self, material_id: int, model_attachment):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_temporary_redirect_material_attachments_by_id_endpoint(
                material_id,
                model_attachment.results[0].attachmentID
            ),
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
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}.'
        assert response.content, "Response content is empty, expected file data"
        assert response.headers.get("Content-Type") is not None, "Content-Type header is missing"
        assert "application/octet-stream" in response.headers["Content-Type"] or "application/" in response.headers[
            "Content-Type"], \
            f"Unexpected Content-Type: {response.headers['Content-Type']}"
        assert f'filename="{model_attachment.results[0].fileName}"' in response.headers["Content-Disposition"], \
            f"Unexpected Content-Disposition: {response.headers['Content-Disposition']}"
        logger.info(f'Successfully get TemporaryRedirect to a temporary link to download a file.')

    @allure.step("Get temporary link for downloading the attachment file from material (noRedirect).")
    def get_downloading_attachment_file_from_material_no_redirect(self, material_id: int, attachment_id: int):
        param = {
            "noRedirect": True
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_temporary_redirect_material_attachments_by_id_endpoint(
                material_id,
                attachment_id
            ),
            params=param,
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
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        assert "application/json" in response.headers["Content-Type"], \
            f"Expected <application/json>, unexpected Content-Type: {response.headers['Content-Type']}"
        model = SuccessGetDownloadMaterialAttachmentModel(**response.json())
        logger.info(f'Successfully get TemporaryRedirect to a temporary link to download a file (noRedirect).')
        return model

    @allure.step("Uploads the file to server and binds it to the material, data from form.")
    def post_upload_attachment_and_bind_to_material_data_from_form(self, material_id: int):
        file_name = f'attachment_from_form{random.randint(1, 999)}.png'
        with io.BytesIO() as image_bytes:
            # Генерация изображения (например, 500x500 пикселей, зеленый фон)
            with Image.new("RGB", (500, 500), color="green") as img:
                img.save(image_bytes, format="PNG")
                image_bytes.seek(0)  # Перемещаем указатель в начало

            payload = MultipartEncoder(
                fields={
                    "Attachments.Index": "0",
                    "Attachments[0].IsPublic": "false",
                    "Attachments[0].IsIgnorePossibleDuplication": "true",
                    "Attachments[0].File": (file_name, image_bytes, 'image/png')
                }
            )
            start = time.time()
            response = requests.post(
                url=self.endpoints.post_upload_material_attachments_from_form_endpoint(material_id),
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
            assert response.status_code == HTTPStatus.CREATED, \
                f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}. {data_response}'
            model = SuccessUploadAttachmentToMaterialModel(results=response.json())
            logger.info(f'Successfully upload {file_name} to material with ID: {material_id}, data from form.')
            return model

    @allure.step("Uploads the file to server and binds it to the task, data from body.")
    def post_upload_attachment_and_bind_to_material_data_from_body(self, material_id: int):
        file_name = f'attachment_from_body{random.randint(1, 99999999)}.png'
        with (io.BytesIO() as image_bytes):
            # Генерация изображения (например, 500x500 пикселей, черный фон)
            with Image.new("RGB", (500, 500), color="black") as img:
                img.save(image_bytes, format="PNG")
                image_bytes.seek(0)  # Перемещаем указатель в начало
                # Преобразование изображения в строку Base64
                image_base64 = base64.b64encode(image_bytes.read()).decode('utf-8')

            payload = {
                "FileName": file_name,
                "ContentType": "image/png",
                "Description": "Файл из тела запроса загружен авто тестом",
                "isPublic": False,
                "File": image_base64
            }
            start = time.time()
            response = requests.post(
                url=self.endpoints.post_upload_material_attachments_from_body_endpoint(material_id),
                headers=self.headers.basic_header(get_token()),
                json=payload
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
                f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}. {data_response}'
            model = AttachmentToMaterialModel(**response.json())
            logger.info(f'Successfully upload {file_name} to material with ID: {material_id}, data from body.')
            return model

    @allure.step("Get list barcodes material by ID.")
    def get_list_barcodes_material_by_id(self, material_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_barcodes_materials_by_id_endpoint(material_id),
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
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = MaterialBarcodesRootModel(root=response.json())
        logger.info(f'Successfully get list barcodes material by ID {material_id}.')
        return model

    @allure.step("Add barcodes to material.")
    def post_add_barcodes_material(self, material_id: int):
        data = {
            "barcodeTypeID": random.randint(1, 8),
            "value": f"{random.randint(1, 999999)}"
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_barcodes_materials_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_barcodes_material_payload(
                material_id, data
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
        model = SuccessAddBarcodesMaterialsModel(results=response.json())
        logger.info(f'Successfully add barcodes to material by ID {material_id}.')
        return model

    @allure.step("Add barcodes to material with barcodeTypeID=1.")
    def post_add_barcodes_material_with_barcode_type_id(self, material_id: int):
        data = {
            "barcodeTypeID": 1,
            "value": f"{random.randint(1, 999999)}"
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_barcodes_materials_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_barcodes_material_payload(
                material_id, data
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
        model = SuccessAddBarcodesMaterialsModel(results=response.json())
        logger.info(f'Successfully add barcodes to material by ID {material_id}.')
        return model

    @allure.step("Add barcodes to material with nonexistent barcodeTypeID.")
    def post_add_barcodes_material_with_nonexistent_barcode_type_id(self, material_id: int):
        data = {
            "barcodeTypeID": random.randint(9, 20),
            "value": f"{random.randint(1, 999999)}"
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_barcodes_materials_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_barcodes_material_payload(
                material_id, data
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
        assert response.status_code == HTTPStatus.CONFLICT, \
            f'Expected status code {HTTPStatus.CONFLICT}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}')
        return None

    @allure.step("Add barcodes to material with empty string in value.")
    def post_add_barcodes_material_with_empty_string_in_value(self, material_id: int):
        data = {
            "barcodeTypeID": random.randint(9, 20),
            "value": f""
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_barcodes_materials_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_barcodes_material_payload(
                material_id, data
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
        assert response.status_code == HTTPStatus.CONFLICT, \
            f'Expected status code {HTTPStatus.CONFLICT}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}')
        return None

    @allure.step("Add two barcodes to material.")
    def post_add_two_barcodes_material(self, material_id: int):
        data = {
            "barcodeTypeID": random.randint(1, 8),
            "value": f"{random.randint(1, 999999)}"
        }
        data2 = {
            "barcodeTypeID": random.randint(1, 8),
            "value": f"{random.randint(1, 999999)}"
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_barcodes_materials_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_barcodes_material_payload(
                material_id, data, data2
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
        model = SuccessAddBarcodesMaterialsModel(results=response.json())
        logger.info(f'Successfully add barcodes to material by ID {material_id}.')
        return model

    @allure.step("Delete barcodes from material by list.")
    def delete_barcodes_from_material_by_list(self, material_id: int, *barcodes_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_barcodes_materials_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_barcodes_from_material_by_list_payload(
                material_id, *barcodes_ids
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
        logger.warning(f'Successfully delete barcodes IDs {barcodes_ids} from material by ID {material_id}.')

    @allure.step("Delete barcode from material by ID.")
    def delete_barcode_from_material_by_id(self, material_id: int, barcode_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_barcodes_materials_by_id_endpoint(material_id, barcode_id),
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
        logger.warning(f'Successfully delete barcode ID {barcode_id} from material by ID {material_id}.')

    @allure.step("Update material barcode.")
    def put_update_material_barcode(self, material_id: int, barcode_id: int):
        model_before = self.get_list_barcodes_material_by_id(material_id)
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_barcodes_materials_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_material_barcode_payload(
                material_id, barcode_id, 2, f"{random.randint(999999, 9999999999999)}"
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
        model_after = self.get_list_barcodes_material_by_id(material_id)
        assert model_before.root[str(material_id)][0].barcodeType.id != model_after.root[str(material_id)][0].barcodeType.id, \
            (f"{model_after.root[str(material_id)][0].barcodeType.id}"
             f"is equal {model_before.root[str(material_id)][0].barcodeType.id}")
        assert model_before.root[str(material_id)][0].value != model_after.root[str(material_id)][0].value, \
            f"{model_after.root[str(material_id)][0].value} is equal {model_before.root[str(material_id)][0].value}"
        logger.info(f'Successfully update material barcode by ID {barcode_id}.')

    @allure.step("Get list materials.")
    def get_list_materials(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_materials_endpoint,
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
            logger.warning("Tenant does not contain materials")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {(HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)}, '
             f'but got {response.status_code}, {data_response}')
        model = SuccessGetListMaterialsListResultModel(results=response.json())
        logger.info(f'Successfully get list materials. Quantity of materials {len(model.results)}.')
        return model

    @allure.step("Head materials.")
    def head_materials(self):
        start = time.time()
        response = requests.head(
            url=self.endpoints.head_materials_endpoint,
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
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        qty_materials = self.get_list_materials_v2_content_range()
        qty_items = int(response.headers["Content-Range"].split("/")[-1])
        assert qty_items == qty_materials, \
            f"Expected qty materials {qty_materials}, but got {qty_items}"
        logger.info(f'Successfully get head materials. Quantity of materials {qty_items}.')
        return qty_items

    @allure.step("Get list materials V2.")
    def get_list_materials_v2(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_materials_v2_endpoint,
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
            logger.warning("Tenant does not contain materials")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {(HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)}, '
             f'but got {response.status_code}, {data_response}')
        model = SuccessGetListMaterialsV2Model(root=response.json())
        logger.info(f'Successfully get list materials V2. Quantity of materials {len(model.root)}.')
        return model

    @allure.step("Get list materials V2 return content range.")
    def get_list_materials_v2_content_range(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_materials_v2_endpoint,
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
            logger.warning("Tenant does not contain materials")
            return None
        assert response.status_code == HTTPStatus.PARTIAL_CONTENT, \
            f'Expected status code {HTTPStatus.PARTIAL_CONTENT}, but got {response.status_code}, {data_response}'
        model = SuccessGetListMaterialsV2Model(root=response.json())
        qty_items = int(response.headers["Content-Range"].split("/")[-1])
        logger.info(f'Successfully get list materials V2. Quantity of materials {len(model.root)}.')
        return qty_items

    @allure.step("Update materials.")
    def put_update_materials(self, material_id: int):
        model_before = self.get_material_by_id(material_id)
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_materials_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_materials_payload(
                material_id,
                f"Измененный материал {random.randint(1, 99999)}",
                currency_id=1,
                unit_id=166,
                erp_name=f"Измененный erpID {random.randint(1, 99999)}"
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
        model_after = self.get_material_by_id(material_id)
        assert model_after.name != model_before.name, \
            f'Name {model_after.name} is equal {model_before.name}. Material has not been updated.'
        assert model_after.erpID != model_before.erpID, \
            f'ErpID {model_after.erpID} is equal {model_before.erpID}. Material has not been updated.'
        logger.info(f'Successfully update materials with ID:{material_id}.')

    @allure.step("Get required list materials.")
    def get_list_required_materials(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_required_materials_endpoint,
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
            logger.warning("Tenant does not contain materials")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {(HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)}, '
             f'but got {response.status_code}, {data_response}')
        model = SuccessGetMaterialsListRequiredResultModel(results=response.json())
        logger.info(f'Successfully get list required materials. Quantity of required materials {len(model.results)}.')
        return model

    @allure.step("Delete material by ID.")
    def delete_material_by_id(self, material_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_material_by_id_endpoint(material_id),
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
        logger.warning(f'Successfully delete material by ID {material_id}.')

    @allure.step("Restore materials by list.")
    def put_restore_materials_by_list(self, *materials_ids: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_materials_restore_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_materials_restore_by_list_payload(*materials_ids)
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
        for material_id in materials_ids:
            model_materials = self.get_material_by_id(material_id)
            if "deleted" in model_materials.model_fields_set:
                raise AttributeError(f"Materials IDs {materials_ids} have not been restored from deleted.")
        logger.info(f'Successfully restore materials by list IDs {materials_ids}.')

    @allure.step("Restore materials by list (undeleted, deleted).")
    def put_restore_materials_by_list_undeleted_deleted(self, *materials_ids: int):
        """Первый не удаленный, второй удаленный."""
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_materials_restore_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_materials_restore_by_list_payload(*materials_ids)
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
        return None

    @allure.step("Restore materials by list (nonexistent, undeleted).")
    def put_restore_materials_by_list_nonexistent_undeleted(self, materials_id: int):
        """Первый ID не созданный, второй не удаленный."""
        qty_materials = self.get_list_materials_v2_content_range()
        nonexistent_material = qty_materials + 1
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_materials_restore_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_materials_restore_by_list_payload(nonexistent_material, materials_id)
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
        assert model.list_model[0].code == "MaterialNotFound", \
            f'Expected <MaterialNotFound>, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "Номенклатура не найдена", \
            f'Expected <Номенклатура не найдена>, but got {model.list_model[0].message}'
        assert "MaterialNotFound" in response.headers["X-Application-Errors"], \
            f'Expected <MaterialNotFound>, but got {response.headers["X-Application-Errors"]}'
        assert "ResourceNotFound" in response.headers["X-ServiceFabric"], \
            f'Expected <ResourceNotFound>, but got {response.headers["X-ServiceFabric"]}'
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Restore materials by list (nonexistent, deleted).")
    def put_restore_materials_by_list_nonexistent_deleted(self, materials_id: int):
        """Первый ID не созданный, второй удаленный."""
        qty_materials = self.get_list_materials_v2_content_range()
        nonexistent_material = qty_materials + 1
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_materials_restore_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_materials_restore_by_list_payload(nonexistent_material, materials_id)
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
        assert model.list_model[0].code == "MaterialNotFound", \
            f'Expected <MaterialNotFound>, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "Номенклатура не найдена", \
            f'Expected <Номенклатура не найдена>, but got {model.list_model[0].message}'
        assert "MaterialNotFound" in response.headers["X-Application-Errors"], \
            f'Expected <MaterialNotFound>, but got {response.headers["X-Application-Errors"]}'
        assert "ResourceNotFound" in response.headers["X-ServiceFabric"], \
            f'Expected <ResourceNotFound>, but got {response.headers["X-ServiceFabric"]}'
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Restore material by ID.")
    def put_restore_material_by_id(self, material_id: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_material_restore_by_id_endpoint(material_id),
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
        model_materials = self.get_material_by_id(material_id)
        if "deleted" in model_materials.model_fields_set:
            raise AttributeError(f"Material ID {material_id} have not been restored from deleted.")
        logger.info(f'Successfully restore material by ID {material_id}.')

    @allure.step("Restore undeleted material by ID.")
    def put_restore_undeleted_material_by_id(self, material_id: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_material_restore_by_id_endpoint(material_id),
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
        return None

    @allure.step("Restore nonexistent material by ID.")
    def put_restore_nonexistent_material_by_id(self):
        qty_materials = self.get_list_materials_v2_content_range()
        nonexistent_material = qty_materials + 1
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_material_restore_by_id_endpoint(nonexistent_material),
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
        assert model.list_model[0].code == "MaterialNotFound", \
            f'Expected <MaterialNotFound>, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "Номенклатура не найдена", \
            f'Expected <Номенклатура не найдена>, but got {model.list_model[0].message}'
        assert "MaterialNotFound" in response.headers["X-Application-Errors"], \
            f'Expected <MaterialNotFound>, but got {response.headers["X-Application-Errors"]}'
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    def post_add_material_negative(self, data: dict, name_step: str, error_message: str):
        with allure.step(name_step):
            start = time.time()
            response = requests.post(
                url=self.endpoints.post_add_materials_endpoint,
                headers=self.headers.basic_header(get_token()),
                json=self.payloads.post_add_three_materials_payload(data)
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
            assert model.list_model[0].code == "InvalidData", \
                f'Expected <InvalidData>, but got {model.list_model[0].code}'
            assert model.list_model[0].message == error_message, \
                f'Expected {error_message}, but got {model.list_model[0].message}'
            assert "InvalidData" in response.headers["X-Application-Errors"], \
                f'Expected <InvalidData>, but got {response.headers["X-Application-Errors"]}'
            logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}')
            return None

    def put_update_material_negative(self, material_id: int, data: dict, name_step: str, error_message: str):
        with allure.step(name_step):
            data["id"] = material_id
            start = time.time()
            response = requests.put(
                url=self.endpoints.post_add_materials_endpoint,
                headers=self.headers.basic_header(get_token()),
                json=self.payloads.put_update_material_payload(data)
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
            assert model.list_model[0].code == "InvalidData", \
                f'Expected <InvalidData>, but got {model.list_model[0].code}'
            assert model.list_model[0].message == error_message, \
                f'Expected {error_message}, but got {model.list_model[0].message}'
            assert "InvalidData" in response.headers["X-Application-Errors"], \
                f'Expected <InvalidData>, but got {response.headers["X-Application-Errors"]}'
            logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}')
            return None

    @allure.step("Get list materials V2 (isDeleted=true).")
    def get_list_deleted_materials_v2(self):
        param = {
            "isDeleted": True
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_materials_v2_endpoint,
            params=param,
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
            logger.warning("Tenant does not contain deleted materials")
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessGetListMaterialsV2Model(root=response.json())
        for material_id, material in model.root.items():
            if "deleted" not in material.model_fields_set:
                raise AssertionError(f"Received not deleted material ID {material_id} in the deleted materials list")
        logger.info(f'Successfully get list deleted materials V2.')
        return model

    @allure.step("Get list materials V2 (isDeleted=false).")
    def get_list_undeleted_materials_v2(self):
        param = {
            "isDeleted": False
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_materials_v2_endpoint,
            params=param,
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
            logger.warning("Tenant does not contain undeleted materials")
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessGetListMaterialsV2Model(root=response.json())
        for material_id, material in model.root.items():
            if "deleted" in material.model_fields_set:
                raise AssertionError(f"Received deleted material ID {material_id} in the undeleted materials list")
        logger.info(f'Successfully get list undeleted materials V2.')
        return model

    @allure.step("Get list materials, searchText=(POST add materials name).")
    def get_list_materials_search_text_new_material(self, material_id: int):
        model_material = self.get_material_by_id(material_id)
        param = {
            "searchText": model_material.name
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_materials_endpoint,
            params=param,
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
        logger.info("The old API endpoint (GET materials) doesn't return the new material data.")

    @allure.step("Get list materials, searchText=(POST add materials erpID).")
    def get_list_materials_search_text_erp_id(self, material_id: int):
        model_material = self.get_material_by_id(material_id)
        param = {
            "searchText": model_material.erpID
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_materials_endpoint,
            params=param,
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
        logger.info("The old API endpoint (GET materials) doesn't return the new material by id data.")

    @allure.step("Get list materials v2, searchText=(POST add materials erpID).")
    def get_list_materials_v2_search_text_erp_id(self, material_id: int):
        model_material = self.get_material_by_id(material_id)
        param = {
            "searchText": model_material.erpID
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_materials_v2_endpoint,
            params=param,
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
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessGetListMaterialsV2Model(root=response.json())
        logger.info(f"Successfully get material by erpID {model_material.erpID}, V2.")
        return model

    @allure.step("Get list materials v2, searchText=(POST add materials name).")
    def get_list_materials_v2_search_text_name(self, material_id: int):
        model_material = self.get_material_by_id(material_id)
        param = {
            "searchText": model_material.name
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_materials_v2_endpoint,
            params=param,
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
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessGetListMaterialsV2Model(root=response.json())
        logger.info(f"Successfully get material by name {model_material.name}, V2.")
        return model
