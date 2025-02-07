import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.es.es_asset_templates.payloads import Payloads
from services.es.es_asset_templates.endpoints import Endpoints
from config.headers import Headers
from services.es.es_asset_templates.models.es_asset_templates_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from random import randint
from PIL import Image
from requests_toolbelt import MultipartEncoder
import io
import base64


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class EsAssetTemplatesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add asset templates with asset type, asset class, location.")
    def post_add_asset_templates(self, asset_type_id: int, asset_class_id: int, location_id: int):
        """Add asset templates with asset type, asset class, location."""
        params = {
            "name": f"Шаблон-{randint(1, 9999)}",
            "description": f"Описание-{randint(1, 9999)}",
            "parentID": None,
            "hostAssetID": None,
            "assetName": None,
            "companyID": None,
            "assetTypeID": asset_type_id,
            "assetClassID": asset_class_id,
            "responsiblePerson": None,
            "scheduleRuleID": None,
            "warrantyTill": None,
            "isMobileAsset": None,
            "locationID": location_id
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_asset_templates_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_add_asset_templates_endpoint(params)
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Code:{response.status_code}.Message:{response.json()}'
        model = SuccessAddAssetTemplatesModel(result=response.json())
        logger.info(f'Successfully add asset templates with ID: {model.result[0]}.')
        return model

    @allure.step("Add asset template, only name and description.")
    def post_add_empty_asset_template(self):
        """Add asset templates, only name and description."""
        params = {
            "name": f"Шаблон-{randint(1, 9999)}",
            "description": f"Описание-{randint(1, 9999)}",
            "parentID": None,
            "hostAssetID": None,
            "assetName": None,
            "companyID": None,
            "assetTypeID": None,
            "assetClassID": None,
            "responsiblePerson": None,
            "scheduleRuleID": None,
            "warrantyTill": None,
            "isMobileAsset": None,
            "locationID": None
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_asset_templates_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_add_asset_templates_endpoint(params)
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Code:{response.status_code}.Message:{response.json()}'
        model = SuccessAddAssetTemplatesModel(result=response.json())
        logger.info(f'Successfully add asset templates with ID: {model.result[0]}.')
        return model

    @allure.step("Update asset templates.")
    def put_update_asset_templates(
            self,
            asset_template_id: int,
            asset_type_id: int or None,
            asset_class_id: int or None,
            location_id: int or None
    ):
        params = {
            "id": asset_template_id,
            "name": f"Обновленный шаблон-{randint(1, 9999)}",
            "description": f"Обновленное описание-{randint(1, 9999)}",
            "parentID": None,
            "hostAssetID": None,
            "assetName": None,
            "companyID": None,
            "assetTypeID": asset_type_id,
            "assetClassID": asset_class_id,
            "responsiblePerson": None,
            "scheduleRuleID": None,
            "warrantyTill": None,
            "isMobileAsset": None,
            "locationID": location_id
        }
        start = time.time()
        response = requests.put(
            url=self.endpoints.post_add_asset_templates_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.put_update_asset_templates_endpoint(params)
        )
        end = time.time()
        data_response = self.response_content(response)
        self.attach_response(data_response)
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}.Message:{data_response}'
        logger.info(f'Successfully update asset templates with ID: {asset_template_id}.')

    @allure.step("Delete asset templates by list.")
    def delete_asset_templates_by_list(self, *asset_templates_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_asset_templates_by_list_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_asset_templates_by_lyst_endpoint(*asset_templates_id)
        )
        end = time.time()
        data_response = self.response_content(response)
        self.attach_response(data_response)
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}. Message:{data_response}'
        logger.warning(f'Successfully delete asset templates with IDs: {asset_templates_id}.')

    @allure.step("Delete asset template by ID.")
    def delete_asset_templates_by_id(self, asset_template_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_asset_template_by_id_endpoint(asset_template_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        data_response = self.response_content(response)
        self.attach_response(data_response)
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected {HTTPStatus.ACCEPTED}, but got {response.status_code}. Message:{data_response}'
        logger.warning(f'Successfully delete asset template with ID: {asset_template_id}.')

    @allure.step("Get list attachments from asset template.")
    def get_list_attachments_from_asset_template(self, asset_template_id: int, deleted: bool):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_attachments_from_asset_template_endpoint(asset_template_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        data_response = self.response_content(response)
        self.attach_response(data_response)
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if deleted is True:
            assert response.status_code == HTTPStatus.NO_CONTENT, \
                f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. Message:{data_response}'
        elif deleted is False:
            assert response.status_code == HTTPStatus.OK, \
                f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. Message:{data_response}'
            model = SuccessGetListAttachmentsFromAssetTemplate(root=response.json())
            logger.info(f'Successfully get list attachments from asset template with ID: {asset_template_id}.')
            return model

    @allure.step("Method to get TemporaryRedirect to a temporary link for downloading the attachment file.")
    def get_downloading_attachment_file_asset_template(self, asset_template_id: int, attachment_id: int, file_name: str):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_attachment_from_asset_template_by_id_endpoint(asset_template_id, attachment_id),
            headers=self.headers.basic_header(API_TOKEN)
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
        assert f'filename="{file_name}"' in response.headers["Content-Disposition"], \
            f"Unexpected Content-Disposition: {response.headers['Content-Disposition']}"
        logger.info(f'Successfully get TemporaryRedirect to a temporary link to download a file.')

    @allure.step("Get temporary link for downloading the attachment file. No Redirect.")
    def get_link_attachment_asset_template_no_redirect(self, asset_template_id: int, attachment_id: int, name: str):
        param = {
            "noRedirect": True
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_attachment_from_asset_template_by_id_endpoint(asset_template_id, attachment_id),
            params=param,
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetAssetTemplatesAttachmentsByIdNoRedirectModel(**response.json())
        assert model.fileName == name, f'Expected file name {name}, but got {model.filename}'
        logger.info(f'Successfully get temporary link to download a file with ID {attachment_id}.')
        return model

    @allure.step("Get deleted attachment file by ID.")
    def get_deleted_attachment_file_asset_template_by_id(self, asset_template_id: int, attachment_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_attachment_from_asset_template_by_id_endpoint(asset_template_id, attachment_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        data_response = self.response_content(response)
        logger.info(response.headers)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.NO_CONTENT, \
            f'Expected status code {HTTPStatus.NO_CONTENT}, but got {response.status_code}, {data_response}'
        logger.info(f'Successfully get deleted attachment file with ID {attachment_id}.')

    @allure.step("Get list attributes from asset template.")
    def get_list_attributes_from_asset_template(self, asset_template_id: int, deleted: bool):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_attributes_asset_template_endpoint(asset_template_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        data_response = self.response_content(response)
        self.attach_response(data_response)
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if deleted is True:
            assert response.status_code == HTTPStatus.NO_CONTENT, \
                f'Expected status code {HTTPStatus.NO_CONTENT}, but got {response.status_code}. {data_response}'
        elif deleted is False:
            assert response.status_code == HTTPStatus.OK, \
                f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. Message:{data_response}'
            model = SuccessAssetTemplateAttributeResultModel(result=response.json())
            logger.info(f'Successfully get list attachments from asset template with ID: {asset_template_id}.')
            return model

    @allure.step("Upload avatar(jpeg > 512x512) to asset template, data from form.")
    def put_upload_avatar_to_asset_template_data_from_form(self, asset_template_id: int):
        file_name = f'avatar_from_form{randint(1, 999)}.JPG'
        with io.BytesIO() as image_bytes:
            # Генерация изображения (например, 600x600 пикселей, красный фон)
            with Image.new("RGB", (600, 600), color="red") as img:
                img.save(image_bytes, format="JPEG")
                image_bytes.seek(0)  # Перемещаем указатель в начало

            payload = MultipartEncoder(
                fields={
                    'File': (file_name, image_bytes, 'image/jpeg')
                }
            )
            start = time.time()
            response = requests.put(
                url=self.endpoints.put_upload_avatar_to_asset_template_data_from_from_endpoint(asset_template_id),
                headers=self.headers.upload_file_header(API_TOKEN, payload.content_type),
                data=payload
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
            assert response.status_code == HTTPStatus.OK, f'Status code {response.status_code}'
            model = SuccessUploadAvatarToAssetTemplateModel(**response.json())
            logger.info(f'Successfully upload {file_name} to asset template with ID: {asset_template_id}.')
            return model

    @allure.step("Upload avatar(jpeg > 512x512) to asset template, data from body.")
    def put_upload_avatar_to_asset_template_data_from_body(self, asset_template_id: int):
        file_name = f'avatar_from_body{randint(1, 999)}.jpg'
        with io.BytesIO() as image_bytes:
            # Генерация изображения (например, 600x600 пикселей, синий фон)
            with Image.new("RGB", (600, 600), color="blue") as img:
                img.save(image_bytes, format="JPEG")
                image_bytes.seek(0)  # Перемещаем указатель в начало
                # Преобразование изображения в строку Base64
                image_base64 = base64.b64encode(image_bytes.read()).decode('utf-8')

            payload = {
                "FileName": file_name,
                "ContentType": "image/jpeg",
                "Description": "Файл загружен авто тестом",
                "File": image_base64
            }
            start = time.time()
            response = requests.put(
                url=self.endpoints.put_upload_avatar_to_asset_template_data_from_body_endpoint(asset_template_id),
                headers=self.headers.basic_header(API_TOKEN),
                json=payload
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
            assert response.status_code == HTTPStatus.OK, f'Status code {response.status_code}'
            model = SuccessUploadAvatarToAssetTemplateModel(**response.json())
            logger.info(f'Successfully upload avatar - {file_name} to asset template with ID: {asset_template_id}.')
            return model

    @allure.step("Delete avatar from the asset template.")
    def delete_avatar_from_asset_template(self, asset_template_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_avatar_from_asset_template_by_id_endpoint(asset_template_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Code:{response.status_code}.Message:{response.json()}'
        logger.warning(f'Successfully delete avatar from the asset template with ID: {asset_template_id}.')

    @allure.step("Delete avatar from the asset templates by list.")
    def delete_avatar_from_asset_templates_by_list(self, *asset_template_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_avatar_from_assets_template_by_list_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_avatar_from_asset_templates_by_lyst_endpoint(*asset_template_ids)
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Code:{response.status_code}.Message:{response.json()}'
        logger.warning(f'Successfully delete avatar by list from the asset template with ID: {asset_template_ids}.')

    @allure.step("Get all list asset templates.")
    def get_all_list_asset_templates(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_asset_templates_endpoint,
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        data_response = self.response_content(response)
        logger.info(response.headers)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning("Asset templates not found")
        else:
            assert response.status_code == HTTPStatus.OK, \
                f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. Message:{data_response}'
            model = SuccessGetListAssetTemplatesModel(root=response.json())
            logger.info(f'Successfully get list asset templates.')
            return model

    @allure.step("Get list asset templates.")
    def get_list_asset_templates(self, *asset_templates_ids: int or None):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_asset_templates_endpoint,
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        data_response = self.response_content(response)
        logger.info(response.headers)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning("Asset templates not found")
        else:
            assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
                (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, but got {response.status_code}.'
                 f'Message:{data_response}')
            model = SuccessGetListAssetTemplatesModel(root=response.json())
            if asset_templates_ids is not None:
                for item in asset_templates_ids:
                    assert str(item) in model.root, \
                        f'Asset template with ID {item} is not in the list asset templates'
            logger.info(f'Successfully get list asset templates.')
            return model

    @allure.step("Get list asset templates check data.")
    def get_list_asset_templates_check_data(self, model_template, *asset_templates_ids: int or None):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_asset_templates_endpoint,
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        data_response = self.response_content(response)
        logger.info(response.headers)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. Message:{data_response}'
        model = SuccessGetListAssetTemplatesModel(root=response.json())
        if asset_templates_ids is not None:
            for item in asset_templates_ids:
                assert str(item) in model.root, \
                    f'Asset template with ID {item} is not in the list asset templates'
                assert model.root[str(item)].name != model_template.name, \
                    f'{model.root[str(item)].name} is equal {model_template.name}'
                assert model.root[str(item)].description != model_template.description, \
                    f'{model.root[str(item)].description} is equal {model_template.description}'
        logger.info(f'Successfully get list asset templates.')
        return model

    @allure.step("Get list asset templates check is deleted.")
    def get_list_asset_templates_check_is_deleted(self, *asset_templates_ids: int or None):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_asset_templates_endpoint,
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        data_response = self.response_content(response)
        logger.info(response.headers)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, but got {response.status_code}.'
             f'Message:{data_response}')
        model = SuccessGetListAssetTemplatesModel(root=response.json())
        if asset_templates_ids is not None:
            for item in asset_templates_ids:
                assert str(item) not in model.root, \
                    f'Asset template with ID {item} is not deleted'
        logger.info(f'Successfully get list asset templates.')
        return model

    @allure.step("Get asset template by ID.")
    def get_asset_template_by_id(self, asset_template_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_asset_template_by_id_endpoint(asset_template_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        data_response = self.response_content(response)
        self.attach_response(data_response)
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Code:{response.status_code}.Message:{response.json()}'
        model = SuccessGetAssetTemplateResult(**response.json())
        logger.info(f'Successfully get asset template with ID: {asset_template_id}.')
        return model

    @allure.step("Get asset template by ID, check avatar.")
    def get_asset_template_by_id_check_avatar(self, asset_template_id: int, model_avatar, deleted: bool):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_asset_template_by_id_endpoint(asset_template_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        data_response = self.response_content(response)
        self.attach_response(data_response)
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Code:{response.status_code}.Message:{response.json()}'
        model = SuccessGetAssetTemplateResult(**response.json())
        if deleted is True:
            assert 'avatarUrl' not in response.json(), \
                f'Avatar with ID {model_avatar.attachmentID} has not been deleted'
        elif deleted is False:
            assert 'avatarUrl' in response.json(), \
                f'Avatar with ID {model_avatar.attachmentID} is not attached to asset template ID {asset_template_id}'
            assert model_avatar.publicUrl == model.avatarUrl, \
                f'Avatar with ID {model_avatar.attachmentID} is not attached to asset template ID {asset_template_id}'
        logger.info(f'Successfully get asset template with ID: {asset_template_id}.')
        return model

    @allure.step("Get deleted asset template by ID.")
    def get_deleted_asset_template_by_id(self, asset_template_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_asset_template_by_id_endpoint(asset_template_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        data_response = self.response_content(response)
        self.attach_response(data_response)
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.NO_CONTENT, \
            f'Expected status code {HTTPStatus.NO_CONTENT}, but got {response.status_code}.Message:{data_response}'
        logger.info(f'Successfully get deleted asset template with ID: {asset_template_id}.')

    @allure.step("Get list districts from asset template.")
    def get_list_districts_from_asset_templates(self, asset_template_id: int, deleted: bool):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_districts_from_asset_template_endpoint(asset_template_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if deleted is True:
            assert response.status_code == HTTPStatus.NO_CONTENT, \
                f'Expected status code {HTTPStatus.NO_CONTENT}, but got {response.status_code}. {data_response}.'
        elif deleted is False:
            assert response.status_code == HTTPStatus.OK, \
                f'Expected {HTTPStatus.OK}, but got {response.status_code}. Message:{data_response}'
            model = SuccessGetListDistrictsFromAssetTemplateModel(root=response.json())
            logger.info(f'Successfully get list districts from asset template with ID: {asset_template_id}.')
            return model

    @allure.step("Get list skills from asset template.")
    def get_list_skills_from_asset_templates(self, asset_template_id: int, deleted: bool):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_skills_from_asset_template_endpoint(asset_template_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if deleted is True:
            assert response.status_code == HTTPStatus.NO_CONTENT, \
                f'Expected {HTTPStatus.NO_CONTENT}, but got {response.status_code}. Message:{data_response}'
        elif deleted is False:
            assert response.status_code == HTTPStatus.OK, \
                f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. Message:{data_response}'
            model = SuccessGetListSkillsFromAssetTemplateModel(result=response.json())
            logger.info(f'Successfully get list skills from asset template with ID: {asset_template_id}.')
            return model

    @allure.step("Get list work types from asset template.")
    def get_list_work_types_from_asset_templates(self, asset_template_id: int, deleted: bool):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_work_types_from_asset_template_endpoint(asset_template_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if deleted is True:
            assert response.status_code == HTTPStatus.NO_CONTENT, \
                f'Expected {HTTPStatus.NO_CONTENT}, but got {response.status_code}.Message:{data_response}'
        elif deleted is False:
            assert response.status_code == HTTPStatus.OK, \
                f'Expected {HTTPStatus.OK}, but got {response.status_code}.Message:{data_response}'
            model = SuccessGetListWorkTypesFromAssetTemplateModel(result=response.json())
            logger.info(f'Successfully get list work types from asset template with ID: {asset_template_id}.')
            return model
