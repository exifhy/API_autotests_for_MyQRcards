import base64
import hashlib
from PIL import Image
import io
from requests import JSONDecodeError
import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.sc.sc_service_contract.payloads import Payloads
from services.sc.sc_service_contract.endpoints import Endpoints
from config.headers import Headers
from services.sc.sc_service_contract.models.sc_service_contract_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token
from src.generators.generators import generator_contract
from requests_toolbelt import MultipartEncoder
from random import randint


class ScServiceContractAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()
        self.contract = next(generator_contract())

    @allure.step("Method for creating or updating service contract(s).")
    def post_method_for_add_contract(self, company_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_method_for_add_contract_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_method_for_add_contract_payload(
                company_id=company_id,
                contract_name=self.contract.name,
                date_from=self.contract.date_from,
                desc=self.contract.description,
                conditions=self.contract.conditions
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}, {response.json()}'
        model = SuccessAddServiceContractModel(contract=response.json())
        logger.info(f'Successfully creating or updating service contract(s).')
        return model

    @allure.step("Method for creating service contract, return description contract.")
    def post_add_contract_return_data_contract(self, company_id: int):
        """Return data created contract."""
        contract_name = self.contract.name
        description_contract = self.contract.description
        conditions_contract = self.contract.conditions
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_method_for_add_contract_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_method_for_add_contract_payload(
                company_id=company_id,
                contract_name=contract_name,
                date_from=self.contract.date_from,
                desc=description_contract,
                conditions=conditions_contract
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}, {response.json()}'
        model = SuccessAddServiceContractModel(contract=response.json())
        logger.info(f'Successfully creating or updating service contract(s).')
        return model.contract[0], contract_name, description_contract, conditions_contract

    @allure.step("Method for deleting a contract by ID.")
    def delete_contract_by_id(self, contract_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_contract_by_id_endpoint(contract_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.warning(f'Successfully deleting a contract by ID: {contract_id}.')

    @allure.step("Method for mass deletion of contracts.")
    def delete_mass_of_contract(self, *args):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_mass_of_contract_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_mass_of_contract_payload(*args)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.warning(f'Successfully mass deleting a contract with IDs: {args}')

    @allure.step("Add a list of objects to the contract.")
    def post_add_list_object_to_contract(self, contract_id: int, asset_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_list_object_to_contract_endpoint(contract_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_list_object_to_contract_payload(
                asset_id=asset_id,
                child=True
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}, {response.json()}'
        model = SuccessAddListObjectsToContractModel(objects=response.json())
        logger.info(f'Successfully add a list of objects to the contract.')
        return model

    @allure.step("Add a list with three objects to the contract.")
    def post_add_list_with_three_objects_to_contract(
            self,
            contract_id: int,
            asset_id_first: int,
            asset_id_second: int,
            asset_id_third: int
    ):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_list_object_to_contract_endpoint(contract_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_list_with_three_objects_to_contract_payload(
                asset1_id=asset_id_first,
                asset2_id=asset_id_second,
                asset3_id=asset_id_third
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}, {response.json()}'
        model = SuccessAddListObjectsToContractModel(objects=response.json())
        logger.info(f'Successfully add a list of objects to the contract with IDs: '
                    f'{asset_id_first}, {asset_id_second}, {asset_id_third}.')
        return model

    @allure.step("Method for updating service contract(s).")
    def put_update_method_for_exist_contract(self, contract_id: int, company_id: int):
        new_contract_name = self.contract.new_name
        new_date_yesterday = self.contract.date_yesterday
        new_desc = self.contract.new_description
        new_conditions = self.contract.new_conditions
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_method_for_exist_contract_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_method_for_update_contract_payload(
                contract_id=contract_id,
                company_id=company_id,
                contract_name=new_contract_name,
                date_from=new_date_yesterday,
                desc=new_desc,
                conditions=new_conditions
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully updating service contract(s).')
        return new_contract_name, new_date_yesterday, new_desc, new_conditions

    @allure.step("Method of get service contract by ID.")
    def get_contract_by_id(self, contract_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_method_of_contract_by_id_endpoint(contract_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, f'Status code {response.status_code}, {response.json()}'
        model = SuccessGetContractResultModel(**response.json())
        logger.info(f'Successfully add a list of objects to the contract.')
        return model

    @allure.step("Method of get list service contracts.")
    def get_list_service_contracts(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_method_list_of_contract_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info(f'NO CONTENT: status code 204.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetMassContractDictModel(root=response.json())
        logger.info(f'Successfully get list service contracts.')
        return model

    @allure.step("Method of get the list of service contract objects.")
    def get_list_of_contract_objects(self, contract_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_of_contract_objects_endpoint(contract_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.PARTIAL_CONTENT, HTTPStatus.OK}, \
            f'Status code {response.status_code}, {response.json()}'
        model = SuccessGetListContractObjectsModel(root=response.json())
        logger.info(f'Successfully get the list of service contract objects.')
        return model

    @allure.step("Method of get the total number of service contracts.")
    def head_method_total_count_of_contract(self):
        start = time.time()
        response = requests.head(
            url=self.endpoints.head_method_total_count_of_contract_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully get the total number of service contracts.')

    @allure.step("Get list user attributes by contract.")
    def get_list_user_attributes_contract(self, contract_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_of_user_attributes_by_contract_endpoint(contract_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning(f'Contract attributes not existed. No content.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessGetContractAttributeResultModel(attributes=response.json())
        logger.info(f'Successfully get a list user attributes by contract.')
        return model

    @allure.step("Method of mass deleting an objects related with a service contract.")
    def delete_objects_related_to_contracts(self, contract_id: int, *args):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_objects_related_to_contracts_endpoint(contract_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_objects_related_to_contracts_payload(*args)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.warning(f'Successfully mass deleting an object related with a service contract with IDs: {args}')

    @allure.step("Method of deleting an object related with a service contract by ID.")
    def delete_objects_related_to_contracts_by_id(self, contract_id: int, asset_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_objects_related_to_contracts_by_id_endpoint(contract_id, asset_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.warning(f'Successfully deleting an object related with a service contract by ID: {asset_id}')

    @allure.step("Method of get the list of service contract objects.")
    def get_list_of_contract_objects(self, contract_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_of_contract_objects_endpoint(contract_id),
            headers=self.headers.basic_header(get_token())
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
            f'Status code {response.status_code}, {response.json()}'
        model = SuccessGetListServiceContractObjectsModel(root=response.json())
        logger.info(f'Successfully get the list of service contract objects.')
        return model

    @allure.step("Add object to contract by ID.")
    def put_add_object_to_contracts_by_id(self, contract_id: int, asset_id: int):
        # params = {
        #     "includeChildren": bool
        # }
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_add_object_to_contracts_by_id_endpoint(contract_id, asset_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}, {response.json()}'
        model = SuccessAddListObjectsToContractModel(objects=response.json())
        logger.info(f'Successfully add object to contract by ID: {asset_id}.')
        return model

    @allure.step("Upload file to server and bind to contract, data from form.")
    def post_upload_file_to_server_and_bind_contract_data_from_form(self, contract_id: int):
        file_name = f'generated_image{randint(1, 99)}.png'
        with io.BytesIO() as image_bytes:
            # Генерация изображения (например, 200x100 пикселей, синий фон)
            with Image.new("RGB", (200, 100), color="blue") as img:
                img.save(image_bytes, format="PNG")
                image_bytes.seek(0)  # Перемещаем указатель в начало

            payload = MultipartEncoder(
                fields={
                    'contractID': f'{contract_id}', 'IsPublic': "false", 'IsIgnorePossibleDuplication': "true",
                    'File': (file_name, image_bytes, 'image/png')
                }
            )
            start = time.time()
            response = requests.post(
                url=self.endpoints.post_upload_file_to_server_and_bind_contract_data_from_form_endpoint(contract_id),
                headers=self.headers.upload_file_header(get_token(), payload.content_type),
                data=payload
            )
            end = time.time()
            logger.info(response.headers)
            try:
                self.attach_response(response.json())
            except JSONDecodeError:
                logger.warning("Received response is not a valid JSON")
            self.attach_time(start, end)
            self.attach_url(response.request.url)
            assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}'
            model = SuccessUploadResultModel(**response.json())
            logger.info(f'Successfully upload file - {file_name} '
                        f'to server and bind to contract with ID: {contract_id}.')
            return model

    @allure.step("Upload file to server and bind to contract, data from body.")
    def post_upload_file_to_server_and_bind_contract_data_from_body(self, contract_id: int):
        file_name = f'generated_image{randint(100, 199)}.png'
        with io.BytesIO() as image_bytes:
            # Генерация изображения (например, 200x100 пикселей, синий фон)
            with Image.new("RGB", (200, 100), color="red") as img:
                img.save(image_bytes, format="PNG")
                image_bytes.seek(0)  # Перемещаем указатель в начало
                # Получение длины содержимого в байтах
                content_length = len(image_bytes.getvalue())
                # Вычисление контрольной суммы MD5
                md5_hash = hashlib.md5(image_bytes.getvalue()).hexdigest()
                # Преобразование изображения в строку Base64
                image_base64 = base64.b64encode(image_bytes.read()).decode('utf-8')

            payload = {
                "Roles": [1, 2, 3],
                "FileName": file_name,
                "ContentType": "image/png",
                "ContentLength": content_length,
                "CheckSum": md5_hash,
                "Description": "Файл загружен авто тестом",
                "IsPublic": True,
                "File": image_base64
            }
            start = time.time()
            response = requests.post(
                url=self.endpoints.post_upload_file_to_server_and_bind_contract_data_from_body_endpoint(contract_id),
                headers=self.headers.basic_header(get_token()),
                json=payload
            )
            end = time.time()
            logger.info(response.headers)
            try:
                self.attach_response(response.json())
            except JSONDecodeError:
                logger.warning("Received response is not a valid JSON")
            self.attach_time(start, end)
            self.attach_url(response.request.url)
            assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}'
            model = SuccessUploadResultModel(**response.json())
            logger.info(f'Successfully upload file - {file_name} '
                        f'to server and bind to contract with ID: {contract_id}.')
            return model

    @allure.step("Method of get the list of attachments bind to contract.")
    def get_list_of_attachments_contract(self, contract_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_attachments_by_contracts_by_id_endpoint(contract_id),
            headers=self.headers.basic_header(get_token())
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
            f'Status code {response.status_code}, {response.json()}'
        model = SuccessGetAttachmentListResultModel(root=response.json())
        logger.info(f'Successfully get the list of attachments bind to contract.')
        return model

    @allure.step("Method of mass attachment bind to a contract.")
    def post_bind_contract_and_attachment_by_list_id(self, contract_id: int, *args):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_bind_contract_and_attachment_by_list_id_endpoint(contract_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_attachment_bind_to_contract_payload(*args)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Status code {response.status_code}, {response.json()}'
        model = SuccessBindAttachmentToContractModel(attachments=response.json())
        logger.info(f'Successfully bind attachment to contract ID: {contract_id}.')
        return model

    @allure.step("Delete attachment from contract.")
    def delete_attachment_from_contract(self, contract_id: int, *args):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_unbind_contract_and_attachment_by_id_endpoint(contract_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_attachment_from_contract_payload(*args)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.warning(f'Successfully deleting an attachment from contract ID: {contract_id}')

    @allure.step("Method of get of attachment binds to contract by id.")
    def get_attachment_bind_contract_by_id(self, contract_id: int, attachment_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_attachment_binds_contract_by_id_endpoint(contract_id, attachment_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, f'Status code {response.status_code}, {response.json()}'
        model = AttachmentListResult(**response.json())
        logger.info(f'Successfully get attachment by ID: {attachment_id} bind to contract by ID: {contract_id}.')
        return model

    @allure.step("Method to get TemporaryRedirect to a temporary link to download a file.")
    def get_temporary_redirect_to_temporary_download_link(self, contract_id: int, attachment_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_temporary_redirect_to_temporary_download_link_endpoint(contract_id, attachment_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Status code {response.status_code}, {response.json()}'
        assert response.content, "Response content is empty, expected file data"
        assert response.headers.get("Content-Type") is not None, "Content-Type header is missing"
        assert "application/octet-stream" in response.headers["Content-Type"] or "application/" in response.headers[
            "Content-Type"], \
            f"Unexpected Content-Type: {response.headers['Content-Type']}"
        logger.info(f'Successfully get TemporaryRedirect to a temporary link to download a file.')

    @allure.step("Method of adding contacts to contracts.")
    def post_add_contacts_to_contract(self, contract_id: int, *args):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_contacts_by_contract_endpoint(contract_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_contacts_to_contract_payload(*args)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}, {response.json()}'
        model = SuccessAddContactsToContractModel(objects=response.json())
        logger.info(f'Successfully adding contacts to contracts.')
        return model

    @allure.step("Method get the list of contacts of those responsible for the contract.")
    def get_list_of_contacts_by_contract(self, contract_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_of_contacts_by_contract_endpoint(contract_id),
            headers=self.headers.basic_header(get_token())
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
            f'Status code {response.status_code}, {response.json()}'
        model = SuccessListContactsResponsibleToContract(root=response.json())
        logger.info(f'Successfully get the list of contacts of those responsible for the contract.')
        return model

    @allure.step("Delete contacts from contract.")
    def delete_contracts_from_contract(self, contract_id: int, *args):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_contacts_by_contract_endpoint(contract_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_contacts_from_contract_payload(*args)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.warning(f'Successfully deleting contacts from contract ID: {args}')

    @allure.step("Delete contact from contract by ID.")
    def delete_contract_from_contract_by_id(self, contract_id: int, contact_id):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_contact_from_contract_by_id_endpoint(contract_id, contact_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.warning(f'Successfully deleting contact by ID: {contact_id} from contract ID: {contract_id}')

    @allure.step("Method of adding contact to contract by ID.")
    def put_add_contact_to_contract_by_id(self, contract_id: int, contact_id):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_contact_to_contract_by_id_endpoint(contract_id, contact_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}, {response.json()}'
        logger.warning(f'Successfully add contact by ID: {contact_id} to contract by ID: {contract_id}')
