import base64
import hashlib
from random import randint
from requests_toolbelt import MultipartEncoder
from PIL import Image
import io
import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.es.asset_attachments.payloads import Payloads
from services.es.asset_attachments.endpoints import Endpoints
from config.headers import Headers
from services.es.asset_attachments.models.es_asset_attachments_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class EsAssetAttachmentsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Bind attachments to asset.")
    def post_bind_attachments_to_asset(self, asset_id: int, *args):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_bind_attachments_to_asset_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.attachments_and_asset_payloads(
                asset_id,
                *args
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
        model = SuccessBindAttachmentsToAssetModel(data=response.json())
        logger.info(f'Successfully bind attachments{args} to asset with ID: {asset_id}.')
        return model

    @allure.step("Unbind attachments from asset.")
    def delete_unbind_attachments_from_asset(self, asset_id: int, *args):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_unbind_attachments_from_asset_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.attachments_and_asset_payloads(
                asset_id,
                *args
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
        logger.warning(f'Successfully unbind attachments{args} from asset with ID: {asset_id}.')

    @allure.step("Upload file to server and bind to asset.")
    def post_upload_file_to_server_and_bind_asset(self, asset_id: int):
        file_name = f'generated_image{randint(299, 399)}.png'
        with io.BytesIO() as image_bytes:
            # Генерация изображения (например, 100x100 пикселей, синий фон)
            with Image.new("RGB", (100, 100), color="green") as img:
                img.save(image_bytes, format="PNG")
                image_bytes.seek(0)  # Перемещаем указатель в начало

            payload = MultipartEncoder(
                fields={
                    'assetID': f'{asset_id}', 'IsPublic': "false", 'IsIgnorePossibleDuplication': "true",
                    'File': (file_name, image_bytes, 'image/png')
                }
            )
            start = time.time()
            response = requests.post(
                url=self.endpoints.post_upload_file_to_asset_endpoint,
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
            model = SuccessAssetAttachmentsUploadResultModel(**response.json())
            logger.info(f'Successfully upload file - {file_name} to server and bind to asset with ID: {asset_id}.')
            return model

    @allure.step("Upload file to server and bind to asset, data from form.")
    def post_upload_file_to_server_and_bind_asset_data_from_form(self, asset_id: int):
        file_name = f'generated_image{randint(300, 499)}.png'
        with io.BytesIO() as image_bytes:
            # Генерация изображения (например, 100x100 пикселей, синий фон)
            with Image.new("RGB", (100, 100), color="black") as img:
                img.save(image_bytes, format="PNG")
                image_bytes.seek(0)  # Перемещаем указатель в начало

            payload = MultipartEncoder(
                fields={
                    'assetID': f'{asset_id}', 'IsPublic': "false", 'IsIgnorePossibleDuplication': "true",
                    'File': (file_name, image_bytes, 'image/png')
                }
            )
            start = time.time()
            response = requests.post(
                url=self.endpoints.post_upload_plan_to_asset_data_from_form_endpoint,
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
            model = SuccessAssetAttachmentsUploadResultModel(**response.json())
            logger.info(f'Successfully upload file - {file_name} to server and bind to asset with ID: {asset_id}.')
            return model

    @allure.step("Upload file to server and bind to asset, data from body.")
    def post_upload_file_to_server_and_bind_asset_data_from_body(self, asset_id: int):
        file_name = f'generated_image{randint(500, 599)}.png'
        with io.BytesIO() as image_bytes:
            # Генерация изображения (например, 200x100 пикселей, синий фон)
            with Image.new("RGB", (200, 200), color="red") as img:
                img.save(image_bytes, format="PNG")
                image_bytes.seek(0)  # Перемещаем указатель в начало
                # Получение длины содержимого в байтах
                content_length = len(image_bytes.getvalue())
                # Вычисление контрольной суммы MD5
                md5_hash = hashlib.md5(image_bytes.getvalue()).hexdigest()
                # Преобразование изображения в строку Base64
                image_base64 = base64.b64encode(image_bytes.read()).decode('utf-8')

            payload = {
                "assetID": asset_id,
                "Roles": [1, 2, 3],
                "FileName": file_name,
                "ContentType": "image/png",
                "CheckSum": md5_hash,
                "Description": "Файл загружен авто тестом",
                "IsPublic": True,
                "File": image_base64
            }
            start = time.time()
            response = requests.post(
                url=self.endpoints.post_upload_attachments_to_asset_data_from_body_endpoint,
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
            model = SuccessAssetAttachmentsUploadResultModel(**response.json())
            logger.info(f'Successfully upload file - {file_name} to server and bind to contract with ID: {asset_id}.')
            return model
