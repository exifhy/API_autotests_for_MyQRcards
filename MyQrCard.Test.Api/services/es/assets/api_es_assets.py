import base64
from PIL import Image
import io
import random
import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from requests_toolbelt import MultipartEncoder
from utils.helper import Helper
from services.es.assets.payloads import Payloads
from services.es.assets.endpoints import Endpoints
from config.headers import Headers
from services.es.assets.models.assets_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token
from faker import Faker
from random import randint
import uuid

fake_ru = Faker('ru_RU')


class EsAssetsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get list assets available to the user.")
    def get_asset_available_to_user(self, param: dict or None, *model_assets: int or None):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_directory_of_objects_available_to_user_endpoint, params=param,
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
            logger.info(f'Successfully receiving the assets list. No content.')
            return None
        else:
            assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
                (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, but got {response.status_code}.'
                 f'Message:{data_response}')
            model = AssetExtResults(results=response.json())
            if model_assets is not None:
                for item in model_assets:
                    assert str(item.id) in model.results, \
                        f'Asset with ID {item.id} is not in the list assets'
            logger.info(f'Successfully receiving the assets list.')
            return model

    @allure.step("Get all list assets available to the user.")
    def get_all_asset_available_to_user(self, param: dict):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_directory_of_objects_available_to_user_endpoint, params=param,
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
            logger.warning("Assets not found")
            return None
        else:
            assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
                (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, but got {response.status_code}.'
                 f'Message:{data_response}')
            model = AssetExtResults(results=response.json())
            logger.info(f'Successfully receiving the assets list.')
            return model

    @allure.step("Object creation.")
    def post_add_object(self, company_id: int, asset_type_id: int, asset_class_id: int):
        name = fake_ru.company()
        notes_text = 'Объект создан авто-тестом'
        start = time.time()
        response = requests.post(
            url=self.endpoints.create_object_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.object_creation_payload(
                parent_id=None,
                name=name,
                company_id=company_id,
                asset_type_id=asset_type_id,
                asset_class_id=asset_class_id,
                notes=notes_text
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
        model = IdNameResultModel(**response.json())
        logger.info(f'Successfully add object without parent object, name object: {name}')
        return model

    @allure.step("Object creation with concurrency stamp.")
    def post_add_object_with_concurrency_stamp(self, company_id: int, asset_type_id: int, asset_class_id: int) -> tuple[IdNameResultModel, str]:
        name = fake_ru.company()
        concurrency_stamp = str(uuid.uuid4())
        notes_text = f'Объект создан авто-тестом c concurrencyStamp {concurrency_stamp}'
        start = time.time()
        response = requests.post(
            url=self.endpoints.create_object_endpoint,
            headers=self.headers.basic_header_with_concurrency_stamp(get_token(), concurrency_stamp),
            json=self.payloads.object_creation_payload(
                parent_id=None,
                name=name,
                company_id=company_id,
                asset_type_id=asset_type_id,
                asset_class_id=asset_class_id,
                notes=notes_text
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
        model = IdNameResultModel(**response.json())
        logger.info(f'Successfully add object with concurrency stamp {concurrency_stamp}, name object: {name}')
        return model, concurrency_stamp

    @allure.step("Object creation with existing concurrency stamp {concurrency_stamp}.")
    def post_add_object_with_existing_concurrency_stamp(self, company_id: int, asset_type_id: int, asset_class_id: int, concurrency_stamp: str):
        name = fake_ru.company()
        notes_text = f'Объект создан авто-тестом c concurrencyStamp {concurrency_stamp}'
        start = time.time()
        response = requests.post(
            url=self.endpoints.create_object_endpoint,
            headers=self.headers.basic_header_with_concurrency_stamp(get_token(), concurrency_stamp),
            json=self.payloads.object_creation_payload(
                parent_id=None,
                name=name,
                company_id=company_id,
                asset_type_id=asset_type_id,
                asset_class_id=asset_class_id,
                notes=notes_text
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
        model = IdNameResultWithConcurrencyStampModel(**response.json())
        logger.warning(f'Not created object with existing concurrency stamp {concurrency_stamp}, name object: {name}')
        return model

    @allure.step("Object creation with responsible person.")
    def post_add_object_with_responsible(
            self, company_id: int, asset_type_id: int, asset_class_id: int, responsible_id: int
    ):
        name = fake_ru.company()
        notes_text = 'Объект создан авто-тестом'
        start = time.time()
        response = requests.post(
            url=self.endpoints.create_object_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.object_creation_with_responsible_payload(
                parent_id=None,
                name=name,
                company_id=company_id,
                asset_type_id=asset_type_id,
                asset_class_id=asset_class_id,
                notes=notes_text,
                responsible_id=responsible_id
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
        model = IdNameResultModel(**response.json())
        logger.info(f'Successfully add object without parent object and with responsible person, name object: {name}')
        return model

    @allure.step("Add child asset.")
    def post_add_child_asset(self, company_id: int, asset_type_id: int, asset_class_id: int, parent_id: int):
        name = fake_ru.company()
        notes_text = 'Дочерний объект создан авто-тестом'
        start = time.time()
        response = requests.post(
            url=self.endpoints.create_object_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.object_creation_payload(
                parent_id=parent_id,
                name=name,
                company_id=company_id,
                asset_type_id=asset_type_id,
                asset_class_id=asset_class_id,
                notes=notes_text
            )
        )
        end = time.time()
        data_response = self.response_content(response)
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        self.attach_response(data_response)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = IdNameResultModel(**response.json())
        logger.info(f'Successfully add child asset, name object: {name}')
        return model

    @allure.step("Add asset with parent.")
    def post_add_asset_with_parent(self, parent_id: int, company_id: int, asset_type_id: int, asset_class_id: int):
        name = fake_ru.company()
        notes_text = 'Объект с родительским объектом создан авто-тестом '
        start = time.time()
        response = requests.post(
            url=self.endpoints.create_object_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.object_creation_payload(
                parent_id=parent_id,
                name=name,
                company_id=company_id,
                asset_type_id=asset_type_id,
                asset_class_id=asset_class_id,
                notes=notes_text
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
        model = IdNameResultModel(**response.json())
        logger.info(f'Successfully add object without parent object, name object: {name}')
        return model

    @allure.step("Update assets by list.")
    def put_update_assets_by_list(self, *args, company_id: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_asset_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_assets_payload(
                *args,
                parent_id=None,
                company_id=company_id
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
        logger.info(f'Successfully update assets with name: {args}')

    @allure.step("Delete object by ID.")
    def delete_object_by_id(self, asset_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_object_by_id_endpoint(asset_id),
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
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.warning(f'Successfully delete the object with ID: {asset_id}.')

    @allure.step("Delete assets by list.")
    def delete_assets_by_list(self, *args):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_assets_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_assets_by_list_payload(*args)
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
        logger.warning(f'Successfully delete the assets with IDs: {args}.')

    @allure.step("Returns the header of a user query with the amount of data that satisfies the filter.")
    def head_assets(self, asset_id: int, checklist_id: int, district_id: int, company_id: int):
        params = {
            "assetID": asset_id,
            "checkListID": checklist_id,
            "districtID": district_id,
            "companyID": company_id
        }
        start = time.time()
        response = requests.head(
            url=self.endpoints.head_asset_endpoint, params=params,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        data_response = self.response_content(response)
        logger.info(response.headers)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        logger.warning(f'Successfully get header asset with ID: {asset_id}.')

    @allure.step("Detailed information on the object by id.")
    def get_detailed_information_on_object_by_id(self, asset_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.detailed_information_on_object_endpoint(asset_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, {response.status_code}, {data_response}'
        model = AssetDetailedInfoResult(**response.json())
        logger.info(f'Successfully receiving the assets detailed info.')
        return model

    @allure.step("Get asset by id.")
    def get_asset_by_id(self, model_asset, deleted_status: bool or None):
        start = time.time()
        response = requests.get(
            url=self.endpoints.detailed_information_on_object_endpoint(model_asset.id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = AssetDetailedInfoResult(**response.json())
        assert model.name == model_asset.name, \
            f'Asset with ID {model_asset.id} has not been created or created with wrong name'
        if deleted_status is True:
            assert 'deleted' in response.json(), \
                f'Asset with ID {model_asset.id} has not been deleted'
        elif deleted_status is False:
            assert 'deleted' not in response.json(), \
                f'Asset with ID {model_asset.id} has not been restore'
        logger.info(f'Successfully get the asset with ID: {model_asset.id}.')
        return model

    @allure.step("Get asset by id, check avatar.")
    def get_asset_by_id_avatar(self, asset_id: int, model_avatar, deleted_status: bool or None):
        start = time.time()
        response = requests.get(
            url=self.endpoints.detailed_information_on_object_endpoint(asset_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = AssetDetailedInfoResult(**response.json())
        if deleted_status is True:
            assert 'avatarUrl' not in response.json(), \
                f'Avatar with ID {model_avatar.attachmentID} has not been deleted'
        elif deleted_status is False:
            assert 'avatarUrl' in response.json(), \
                f'Avatar with ID {model_avatar.attachmentID} is not attached to asset with ID {asset_id}'
            assert model_avatar.publicUrl == model.avatarUrl, \
                f'Avatar with ID {model_avatar.attachmentID} is not attached to asset with ID {asset_id}'
        logger.info(f'Successfully get the asset with ID: {asset_id}.')
        return model

    @allure.step("Method of publishing an object.")
    def put_method_of_publishing_an_object_by_id(self, asset_id: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.method_of_publishing_an_object_endpoint(asset_id),
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
            f'Expected {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.info(f'Successful publication of the object with ID {asset_id}.')

    @allure.step("Method of unpublishing of an asset.")
    def put_method_of_unpublishing_asset_by_id(self, asset_id: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_of_unpublishing_an_object_endpoint(asset_id),
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
        logger.info(f'Successful unpublish of an asset with ID: {asset_id}.')

    @allure.step("Method of publishing an object without bind location.")
    def put_method_of_publishing_an_object_by_id_without_location(self, asset_id: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.method_of_publishing_an_object_endpoint(asset_id),
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
            f'Expected status code {HTTPStatus.CONFLICT}, but got {response.status_code},{data_response}'
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].code == 'InvalidOperation', \
            f'Expected InvalidOperation, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "Недопустимая операция: Хост-объект должен иметь локацию", \
            f'Expected Недопустимая операция: Хост-объект должен иметь локацию, but got {model.list_model[0].message}'
        assert "InvalidOperation" in response.headers["X-Application-Errors"], \
            f'Expected InvalidOperation, but got {response.headers["X-Application-Errors"]}'
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')

    @allure.step("Update the object by ID.")
    def put_update_object_by_id(self, asset_id: int, company_id: int, asset_type_id: int, asset_class_id: int):
        new_name = f'Изменение имени авто-тестом-{random.randint(1, 999)}'
        new_notes = f'Изменение описания авто-тестом-{random.randint(1, 999)}'
        start = time.time()
        response = requests.put(
            url=self.endpoints.update_object_endpoint(asset_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.object_creation_payload(
                parent_id=None,
                name=new_name,
                company_id=company_id,
                asset_type_id=asset_type_id,
                asset_class_id=asset_class_id,
                notes=new_notes
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
        logger.info(f'Successful update the object, new name object: {new_name}')

    @allure.step("Get the list of assignments of the specified asset to users.")
    def get_list_assignment_of_asset_to_user(self, asset_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_assignments_asset_to_user_endpoint(asset_id),
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
            logger.warning(f'Status code: {response.status_code}')
        else:
            assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT, HTTPStatus.NO_CONTENT}, \
                f'Status code {response.status_code}, {data_response}'
            model = SuccessGetListAttachmentResultModel(**response.json())
            logger.info(f'Successfully get the list of assignments of the specified asset to users.')
            return model

    @allure.step("Get the list asset attachments.")
    def get_list_asset_attachments(self, asset_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_attachments_bind_to_asset_endpoint(asset_id),
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
            logger.warning("Tenant does not contain list asset attachments")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT},'
             f'but got {response.status_code}, {data_response}')
        model = SuccessGetListAttachmentResultModel(root=response.json())
        logger.info(f'Successfully get the list asset attachments.')
        return model

    @allure.step("Get asset attachment by id.")
    def get_list_asset_attachment_by_id(self, asset_id: int, attach_id):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_attachment_bind_to_asset_by_id_endpoint(asset_id, attach_id),
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
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT},'
             f'but got {response.status_code}, {data_response}')
        assert response.content, "Response content is empty, expected file data"
        assert response.headers.get("Content-Type") is not None, "Content-Type header is missing"
        assert "application/octet-stream" in response.headers["Content-Type"] or "application/" in response.headers[
            "Content-Type"], \
            f"Unexpected Content-Type: {response.headers['Content-Type']}"
        expected_min_size = 1  # Минимальный размер файла (в байтах)
        assert len(response.content) >= expected_min_size, "Downloaded file size is smaller than expected"
        logger.info(f'Successfully get asset attachment by iD: {attach_id}.')

    @allure.step("Get the list asset attributes.")
    def get_list_asset_attributes(self, asset_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_of_user_attributes_by_asset_endpoint(asset_id),
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
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT},'
             f'but got {response.status_code}, {data_response}')
        model = SuccessGetListAssetAttributeResultModel(result=response.json())
        logger.info(f'Successfully get the list asset attributes.')
        return model

    @allure.step(
        "Upload a JPG image of at least 128x128 to be used as an avatar for asset, data from the form."
    )
    def put_upload_avatar_for_asset_data_from_form(self, asset_id: int):
        file_name = f'generated_image{randint(800, 899)}.png'
        with io.BytesIO() as image_bytes:
            # Генерация изображения (например, 200x100 пикселей, синий фон)
            with Image.new("RGB", (128, 128), color="black") as img:
                img.save(image_bytes, format="PNG")
                image_bytes.seek(0)  # Перемещаем указатель в начало

            payload = MultipartEncoder(
                fields={
                    'File': (file_name, image_bytes, 'image/png')
                }
            )
            start = time.time()
            response = requests.put(
                url=self.endpoints.put_upload_avatar_attachment_from_form_endpoint(asset_id),
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
            assert response.status_code == HTTPStatus.OK, f'Status code {response.status_code}'
            model = SuccessPutUploadFileModel(**response.json())
            logger.info(f'Successfully upload file - {file_name} to asset with ID: {asset_id} data from form.')
            return model

    @allure.step(
        "Upload a JPG image of at least 128x128 to be used as an avatar for asset, data from the body."
    )
    def put_upload_avatar_for_asset_data_from_body(self, asset_id: int):
        file_name = f'generated_image{randint(900, 999)}.png'
        with io.BytesIO() as image_bytes:
            # Генерация изображения (например, 200x100 пикселей, синий фон)
            with Image.new("RGB", (128, 128), color="red") as img:
                img.save(image_bytes, format="PNG")
                image_bytes.seek(0)  # Перемещаем указатель в начало
                # Преобразование изображения в строку Base64
                image_base64 = base64.b64encode(image_bytes.read()).decode('utf-8')

            payload = {
                "FileName": file_name,
                "ContentType": "image/png",
                "File": image_base64
            }
            start = time.time()
            response = requests.put(
                url=self.endpoints.put_upload_avatar_attachment_from_body_endpoint(asset_id),
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
            assert response.status_code == HTTPStatus.OK, f'Status code {response.status_code}'
            model = SuccessPutUploadFileModel(**response.json())
            logger.info(f'Successfully upload file - {file_name} to asset with ID: {asset_id} data form body.')
            return model

    @allure.step("Delete avatar from asset by ID.")
    def delete_avatar_from_asset_by_id(self, asset_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_avatar_asset_by_id_endpoint(asset_id),
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
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.warning(f'Successfully delete the avatar from asset with ID: {asset_id}.')

    @allure.step("Delete avatar from asset by list.")
    def delete_avatar_from_asset_by_list(self, *args):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_assets_avatar_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_avatar_from_assets_payloads(*args)
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
        logger.warning(f'Successfully delete the avatar from asset with ID: {args}.')

    @allure.step("Get the list asset checklists.")
    def get_list_asset_checklists(self, asset_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_asset_checklist_endpoint(asset_id),
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
             f'but got {response.status_code}, {data_response}')
        model = SuccessGetAssetChecklistsModel(root=response.json())
        logger.info(f'Successfully get the list asset checklists.')
        return model

    @allure.step("Add checklists to asset by list.")
    def post_add_checklists_to_asset_by_list(self, asset_id: int, *args):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_checklists_to_asset_by_list_endpoint(asset_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_checklist_to_asset_payloads(*args)
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
        logger.info(f'Successfully add checklists to asset by list with iD {args}.')

    @allure.step("Delete checklists from asset by list.")
    def delete_checklists_from_asset_by_list(self, asset_id: int, *args):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_checklist_from_asset_endpoint(asset_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_checklists_from_asset_payloads(*args)
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
        logger.warning(f'Successfully delete checklists from asset by list with iD {args}.')

    @allure.step("Add checklist to asset by ID.")
    def post_add_checklist_to_asset_by_id(self, asset_id: int, checklist_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_checklist_to_asset_by_id_endpoint(asset_id, checklist_id),
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
        logger.info(f'Successfully add checklist to asset with iD {checklist_id}.')

    @allure.step("Delete checklists from asset by ID.")
    def delete_checklist_from_asset_by_id(self, asset_id: int, checklist_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_checklist_from_asset_by_id_endpoint(asset_id, checklist_id),
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
        logger.warning(f'Successfully delete checklist from asset with iD {checklist_id}.')

    @allure.step("Get a list of valid contacts for the asset.")
    def get_list_valid_contacts_for_asset(self, asset_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_valid_contacts_for_asset_endpoint(asset_id),
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
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT},'
             f'but got {response.status_code}, {data_response}')
        model = SuccessGetAssetContactsResultModel(**response.json())
        logger.info(f'Successfully get a list of valid contacts for the asset with ID: {asset_id}.')
        return model

    @allure.step("Get valid contact for the asset by ID.")
    def get_valid_contact_for_asset_by_id(self, asset_id: int, contact_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_asset_contact_by_id_endpoint(asset_id, contact_id),
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
        model = SuccessGetAssetContactByIdResult(**response.json())
        logger.info(f'Successfully get valid contact for the asset with ID: {contact_id}.')
        return model

    @allure.step("Add a contact person for the asset.")
    def post_add_contact_person_for_asset(self, asset_id: int, contact_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_contact_to_asset_endpoint(asset_id, contact_id),
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
        model = SuccessListContactAssetResultModel(result=response.json())
        logger.info(f'Successfully add a contact person for the asset with ID: {contact_id}.')
        return model

    @allure.step("Delete contact person from asset by ID.")
    def delete_contact_person_from_asset_by_id(self, asset_id: int, contact_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_contact_from_asset_by_id_endpoint(asset_id, contact_id),
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
        logger.warning(f'Successfully delete contact person from the asset with ID: {contact_id}.')

    @allure.step("Add a contact persons for asset by list.")
    def post_add_contact_persons_for_asset(self, asset_id: int, *args):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_contacts_to_asset_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.contact_persons_for_asset_payload(asset_id, *args)
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
        model = SuccessListContactAssetResultModel(result=response.json())
        logger.warning(f'Successfully add contact personas for the asset with ID: {args}.')
        return model

    @allure.step("Delete contact persons from asset by list.")
    def delete_contact_persons_from_asset_by_list(self, asset_id: int, *args):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_contacts_from_asset_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.contact_persons_for_asset_payload(asset_id, *args)
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
        logger.warning(f'Successfully delete contact persons from the asset with ID: {args}.')

    @allure.step("Delete the asset and all child assets by ID.")
    def delete_asset_and_child_assets_by_id(self, asset_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_asset_and_all_child_assets_by_id_endpoint(asset_id),
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
        logger.warning(f'Successfully delete the asset and all child assets with ID: {asset_id}.')

    @allure.step("Delete the assets and all child assets by list.")
    def delete_assets_and_child_assets_by_list(self, *args):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_assets_and_all_child_assets_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_assets_and_all_child_assets_by_list_payload(*args)
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
        logger.warning(f'Successfully delete the assets and all child assets with ID: {args}.')

    @allure.step("Restores deleted assets by list.")
    def put_restores_deleted_assets_by_list(self, *args):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_restore_assets_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_restores_deleted_assets_by_list_payload(*args)
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
        logger.info(f'Successfully restore the assets with ID: {args}.')

    @allure.step("Get the list of districts for the asset.")
    def get_list_districts_for_asset(self, asset_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_districts_for_asset_endpoint(asset_id),
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
             f'but got {response.status_code}, {data_response}')
        model = SuccessAssetDistrictResultModel(root=response.json())
        logger.info(f'Successfully get the list of districts for the asset with ID: {asset_id}.')
        return model

    @allure.step("Get the current location of the asset.")
    def get_actual_locations_of_asset(self, asset_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_actual_locations_asset_endpoint(asset_id),
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
             f'but got {response.status_code}, {data_response}')
        model = LocationResult(**response.json())
        logger.info(f'Successfully get the current location of the asset with ID: {asset_id}.')
        return model

    @allure.step("Get a list of the asset skills.")
    def get_list_skill_of_asset(self, asset_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_asset_skills_endpoint(asset_id),
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
             f'but got {response.status_code}, {data_response}')
        model = SuccessAssetSkillResultModel(root=response.json())
        logger.info(f'Successfully get a list of the asset skills with ID: {asset_id}.')
        return model

    @allure.step("Get a list of active (not deleted) tags by asset.")
    def get_list_active_tags_by_asset(self, asset_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_active_tags_by_asset_endpoint(asset_id),
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
            logger.warning("Status code - NO CONTENT(204)")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT},'
             f'but got {response.status_code}, {data_response}')
        model = SuccessGetTagsAssetsModel(result=response.json())
        logger.info(f'Successfully get a list of active (not deleted) tags by asset with ID: {asset_id}.')
        return model

    @allure.step("Get a list of work types available for the asset.")
    def get_list_asset_work_types(self, asset_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_work_types_by_asset_endpoint(asset_id),
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
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT},'
             f'but got {response.status_code}, {data_response}')
        model = SuccessGetAssetWorkTypesResult(root=response.json())
        logger.info(f'Successfully get a list of work types available for the asset with ID: {asset_id}.')
        return model
