import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.es.es_asset_template_attachments.payloads import Payloads
from services.es.es_asset_template_attachments.endpoints import Endpoints
from config.headers import Headers
from services.es.es_asset_template_attachments.models.es_asset_template_attachments_model import *
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


class EsAssetTemplateAttachmentsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Bind attachments to asset templates by list.")
    def post_bind_attachments_to_asset_template(self, asset_template_id: int, *attachment_ids: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_bind_attachments_to_asset_template_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_bind_attachments_to_asset_template_payload(
                asset_template_id,
                *attachment_ids
            )
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
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Code:{response.status_code}.Message:{response.json()}'
        model = SuccessBindAttachmentsToAssetTemplateModel(result=response.json())
        logger.info(
            f'Successfully bind attachments to template with ID: {asset_template_id}, attachment ID: {attachment_ids}')
        return model

    @allure.step("Delete attachments from asset templates by list.")
    def delete_attachments_from_asset_template(self, asset_template_id: int, *attachment_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_attachments_from_asset_template_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_attachments_from_asset_template_payload(
                asset_template_id,
                *attachment_ids
            )
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}. Message:{data_response}'
        logger.warning(
            f'Successfully delete attachments from template with ID: {asset_template_id}, '
            f'attachment ID: {attachment_ids}'
        )

    @allure.step("Upload and bind attachment to asset template data from form.")
    def post_upload_and_bind_to_asset_template_data_from_form(self, asset_template_id: int):
        file_name = f'attachment_from_form{randint(1, 999)}.jpg'
        with (io.BytesIO() as image_bytes):
            # Генерация изображения (например, 200x200 пикселей, зеленый фон)
            with Image.new("RGB", (200, 200), color="green") as img:
                img.save(image_bytes, format="JPEG")
                image_bytes.seek(0)  # Перемещаем указатель в начало

            payload = MultipartEncoder(
                fields={
                    "AssetTemplateID": f"{asset_template_id}",
                    "IsPublic": "false",
                    "IsIgnorePossibleDuplication": "true",
                    'File': (file_name, image_bytes, 'image/jpeg')
                }
            )
            start = time.time()
            response = requests.post(
                url=self.endpoints.post_upload_attachment_to_template_data_from_form_endpoint,
                headers=self.headers.upload_file_header(API_TOKEN, payload.content_type),
                data=payload
            )
            end = time.time()
            data_response = self.response_content(response)
            logger.info(response.headers)
            self.attach_response(data_response)
            self.attach_response_headers(response.headers)
            self.attach_time(start, end)
            self.attach_url(response.request.url)
            assert response.status_code == HTTPStatus.CREATED, \
                f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
            model = SuccessUploadBindAttachmentToTemplateModel(**response.json())
            logger.info(f'Successfully upload {file_name} to asset template with ID: {asset_template_id}.')
            return model

    @allure.step("Upload and bind attachment to asset template, data from body.")
    def post_upload_bind_attachment_to_asset_template_data_from_body(self, asset_template_id: int):
        file_name = f'attachment_from_body{randint(1, 999)}.png'
        with io.BytesIO() as image_bytes:
            # Генерация изображения (например, 200x200 пикселей, черный фон)
            with Image.new("RGB", (200, 200), color="black") as img:
                img.save(image_bytes, format="PNG")
                image_bytes.seek(0)  # Перемещаем указатель в начало
                # Преобразование изображения в строку Base64
                image_base64 = base64.b64encode(image_bytes.read()).decode('utf-8')

            payload = {
                "assetTemplateID": asset_template_id,
                "FileName": file_name,
                "ContentType": "image/png",
                "Description": "Файл загружен авто тестом",
                "isPublic": False,
                "IsIgnorePossibleDuplication": True,
                "File": image_base64
            }
            start = time.time()
            response = requests.post(
                url=self.endpoints.post_upload_attachment_to_template_data_from_body_endpoint,
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
            assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}'
            model = SuccessUploadBindAttachmentToTemplateModel(**response.json())
            logger.info(f'Successfully upload {file_name} to asset template with ID: {asset_template_id}.')
            return model
