from random import randint
from requests_toolbelt import MultipartEncoder
from PIL import Image
import io
import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.common.common_attachments.payloads import Payloads
from services.common.common_attachments.endpoints import Endpoints
from config.headers import Headers
from services.common.common_attachments.models.common_attachments_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class CommonAttachmentsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Upload file to server, data from form.")
    def post_upload_attachments_to_server_data_from_form(self):
        file_name = f'generated_image{randint(600, 699)}.png'
        with io.BytesIO() as image_bytes:
            # Генерация изображения (например, 100x100 пикселей, синий фон)
            with Image.new("RGB", (100, 100), color="green") as img:
                img.save(image_bytes, format="PNG")
                image_bytes.seek(0)  # Перемещаем указатель в начало

            payload = MultipartEncoder(
                fields={
                    'IsPublic': "true", 'IsIgnorePossibleDuplication': "true",
                    'File': (file_name, image_bytes, 'image/png')
                }
            )
            start = time.time()
            response = requests.post(
                url=self.endpoints.post_upload_attachments_to_server_endpoint,
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
            model = SuccessUploadAttachmentsToServerDataFromFormModel(**response.json())
            logger.info(f'Successfully upload file - {file_name} to server.')
            return model

    @allure.step("Delete attachment by ID.")
    def delete_attachment_by_id(self, attachment_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_attachment_endpoint(attachment_id),
            headers=self.headers.basic_header(API_TOKEN)
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
        logger.warning(f'Successfully delete attachment by ID: {attachment_id}.')
