from PIL import Image
import io
import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from requests_toolbelt import MultipartEncoder
from utils.helper import Helper
from services.es.es_asset_schemas.payloads import Payloads
from services.es.es_asset_schemas.endpoints import Endpoints
from config.headers import Headers
from services.es.es_asset_schemas.models.es_asset_schemas_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from random import randint

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class EsAssetSchemasAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Returns the asset scheme attached to the asset.")
    def get_asset_scheme_attached_to_asset(self, asset_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_plan_scheme_attached_to_asset_endpoint(asset_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Code:{response.status_code}.Message:{response.json()}'
        model = SuccessGetAssetSchemaModel(**response.json())
        logger.info(f'Successfully get the asset-scheme attached to the asset with ID: {asset_id}.')
        return model

    @allure.step("Returns a list of existing asset-scheme for the current asset and all available asset up the tree.")
    def get_asc_list_asset_scheme_for_asset(self, asset_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_existing_asset_schemas_endpoint(asset_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Code:{response.status_code}.Message:{response.json()}'
        model = SuccessGetListAssetSchemasModel(root=response.json())
        logger.info(f'Successfully a list of existing asset-scheme for the current asset with ID: {asset_id}.')
        return model

    @allure.step("Returns the asset-scheme by ID.")
    def get_plan_scheme_by_id(self, schema_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_asset_schema_by_id_endpoint(schema_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Code:{response.status_code}.Message:{response.json()}'
        model = SuccessGetAssetSchemaModel(root=response.json())
        logger.info(f'Successfully get the asset-scheme with ID: {schema_id}.')
        return model

    @allure.step("Delete the asset-scheme by ID.")
    def delete_asset_scheme_by_id(self, schema_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_asset_schema_by_id_endpoint(schema_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Code:{response.status_code}.Message:{response.json()}'
        logger.warning(f'Successfully delete the asset-scheme with ID: {schema_id}.')

    @allure.step("Update the asset-schemes, change name scheme.")
    def put_update_asset_scheme(self, asset_id: int, scheme_id: int):
        name = f'Обновленная план схема-{randint(1, 999)}'
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_asset_schemas_endpoint(asset_id),
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.put_update_asset_scheme_payload(scheme_id, name)
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Code:{response.status_code}.Message:{response.json()}'
        model = SuccessUpdateAssetSchemeModel(**response.json())
        logger.info(f'Successfully update name {model.name} the asset-scheme with ID: {model.id}.')
        return model

    @allure.step("Create asset-scheme.")
    def post_add_asset_scheme(self, asset_id: int, scheme_id: int, image_id: int):
        asset_x = 1
        asset_y = 1
        name = f'План схема-{randint(1, 999)}'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_asset_schemas_endpoint(asset_id),
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_create_asset_scheme_payload(
                asset_id, asset_x, asset_y, scheme_id, asset_id, image_id, name
            )
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Code:{response.status_code}.Message:{response.json()}'
        model = SuccessCreateAssetSchemeModel(**response.json())
        logger.info(f'Successfully create asset-scheme with ID: {model.id}, asset ID: {asset_id}, name {model.name}.')
        return model

    @allure.step("Create asset-scheme only name.")
    def post_add_asset_scheme_only_name(self, asset_id: int):
        name = f'План схема-{randint(1, 999)}'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_asset_schemas_endpoint(asset_id),
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_create_asset_scheme_only_name_payload(name)
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Code:{response.status_code}.Message:{response.json()}'
        model = SuccessCreateAssetSchemeModel(**response.json())
        logger.info(f'Successfully create asset-scheme with name: {model.name}, with ID: {model.id}.')
        return model

    @allure.step("Get a list of asset schemes available to the user.")
    def get_list_asset_schemes_available_to_user(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_asset_schemas_endpoint,
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Code:{response.status_code}.Message:{response.json()}'
        model = SuccessGetListAssetSchemesAvailableToUser(root=response.json())
        logger.info(f'Successfully get a list of asset schemes available to the user.')
        return model

    @allure.step("Bind asset schemes to asset by list.")
    def post_bind_asset_schemes_to_asset_by_list(self, scheme_id: int, *asset_ids: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_bind_asset_schemas_to_asset_by_id_endpoint(scheme_id),
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_bind_asset_scheme_to_asset_payloads(*asset_ids)
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Code:{response.status_code}.Message:{response.json()}'
        logger.info(f'Successfully bind asset schemes to asset by list with IDs: {asset_ids}.')

    @allure.step("Unbind asset scheme from asset by list.")
    def put_unbind_asset_scheme_from_assets_by_list(self, scheme_id: int, *asset_ids: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_unbind_asset_schemas_from_asset_by_id_endpoint(scheme_id),
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.put_unbind_asset_scheme_to_asset_payloads(*asset_ids)
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Code:{response.status_code}.Message:{response.json()}'
        logger.info(f'Successfully unbind asset scheme with ID: {scheme_id} from assets by list: {asset_ids}.')

    @allure.step("Gets information about the picture attached to the asset-scheme.")
    def get_info_picture_attached_to_asset_scheme(self, scheme_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_data_image_bind_asset_schemas_by_id_endpoint(scheme_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Code:{response.status_code}.Message:{response.json()}'
        model = SuccessAssetSchemaImageModel(**response.json())
        logger.info(f'Successfully get the asset-scheme with ID: {scheme_id}.')
        return model

    @allure.step("Delete the current view (picture) associated with the asset-scheme.")
    def delete_picture_associated_with_asset_scheme(self, scheme_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_image_bind_asset_schemas_by_id_endpoint(scheme_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Code:{response.status_code}.Message:{response.json()}'
        logger.warning(f'Successfully delete the current picture associated with the asset-scheme ID: {scheme_id}.')

    @allure.step("Method to get TemporaryRedirect to a temporary link for downloading the attached plan file.")
    def get_temporary_link_for_downloading_attached_plan_file(self, scheme_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_image_bind_asset_schemas_temporary_redirect_by_id_endpoint(scheme_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
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

    @allure.step("Upload file to server and bind to asset scheme, data from form.")
    def post_upload_file_to_server_and_bind_asset_scheme_data_from_form(self, scheme_id: int):
        file_name = f'generated_image{randint(999, 1099)}.JPG'
        with io.BytesIO() as image_bytes:
            # Генерация изображения (например, 200x200 пикселей, зеленый фон)
            with Image.new("RGB", (200, 200), color="green") as img:
                img.save(image_bytes, format="JPEG")
                image_bytes.seek(0)  # Перемещаем указатель в начало

            payload = MultipartEncoder(
                fields={
                    'IsIgnorePossibleDuplication': "false",
                    'File': (file_name, image_bytes, 'image/jpg')
                }
            )
            start = time.time()
            response = requests.post(
                url=self.endpoints.post_upload_file_add_asset_schema_from_form_endpoint(scheme_id),
                headers=self.headers.upload_file_header(API_TOKEN, payload.content_type),
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
            model = SuccessUploadFileToAssetSchemeModel(**response.json())
            logger.info(f'Successfully upload {file_name} to server and bind to asset scheme with ID: {scheme_id}.')
            return model

    @allure.step("Bind attachment to asset scheme if attachment upload from common service.")
    def post_bind_attachment_to_asset_scheme(self, scheme_id: int, attachment_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_bind_image_to_asset_schema_by_id_endpoint(scheme_id, attachment_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Code:{response.status_code}.Message:{response.json()}'
        model = SuccessBindAttachmentToAssetSchemeModel(**response.json())
        logger.info(f'Successfully bind attachment with ID: {attachment_id} to asset scheme with ID: {scheme_id}.')
        return model

    @allure.step("Returns the complete list of task points placed on the asset scheme.")
    def get_list_points_from_asset_schema(self, scheme_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_points_from_asset_schema_endpoint(scheme_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Code:{response.status_code}.Message:{response.json()}'
        model = SuccessGetListPointsPlacedOnAssetSchemeModel(result=response.json())
        logger.info(f'Successfully get list of task points placed on the asset scheme with ID: {scheme_id}.')
        return model

    @allure.step("Adds points to the asset scheme.")
    def post_add_points_to_asset_schema(self, scheme_id: int, task_id: int):
        params = {
            "taskID": task_id,
            "y": 100,
            "x": 100
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_points_to_asset_schema_endpoint(scheme_id),
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_add_points_to_asset_schema_payload(params)
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.OK, \
            f'Code:{response.status_code}.Message:{response.json()}'
        model = SuccessGetListPointsPlacedOnAssetSchemeModel(result=response.json())
        logger.info(f'Successfully adds points to the asset scheme with ID: {scheme_id}, task ID: {task_id}.')
        return model

    @allure.step("Delete points from the asset scheme by list.")
    def delete_points_from_asset_schema_by_list(self, scheme_id: int, *point_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_points_from_asset_schema_by_list_endpoint(scheme_id),
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_points_from_asset_schema_payload(*point_id)
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Code:{response.status_code}.Message:{response.json()}'
        logger.warning(f'Successfully delete points with ID: {point_id} from the asset scheme with ID: {scheme_id}.')
