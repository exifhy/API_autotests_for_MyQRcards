from requests import JSONDecodeError
import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.work.work_completed_work_attachments.payloads import Payloads
from services.work.work_completed_work_attachments.endpoints import Endpoints
from config.headers import Headers
from services.work.work_completed_work_attachments.models.work_completed_work_attachments_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from random import randint
from requests_toolbelt import MultipartEncoder
from PIL import Image
import io
import base64

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class WorkCompletedWorkAttachmentsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Adds a uploaded attachments file to a completed work.")
    def post_completed_work_attachments(self, task_id: int, completed_work_id: int, attachment_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_completed_work_attachments_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_completed_work_attachments_payload(
                task_id,
                completed_work_id,
                attachment_id
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
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}, {response.json()}'
        model = SuccessCompletedWorkAttachmentsModel(result=response.json())
        logger.info(f'Successfully adds a uploaded attachments with ID: {attachment_id}'
                    f' file to a completed work ID: {completed_work_id}.')
        return model

    @allure.step("Delete a uploaded attachments file from completed work.")
    def delete_completed_work_attachments(self, task_id: int, completed_work_id: int, attachment_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_completed_work_attachments_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_completed_work_attachments_payload(
                task_id,
                completed_work_id,
                attachment_id
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
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.warning(f'Successfully delete uploaded attachments file with ID: {attachment_id}'
                       f' from completed work with ID: {completed_work_id}.')

    @allure.step("Uploads the file to server and binds it to the completed work, data from form.")
    def post_upload_and_bind_to_completed_work_data_from_form(self, task_id: int, completed_work_id: int):
        file_name = f'attachment_from_form{randint(1, 999)}.png'
        with io.BytesIO() as image_bytes:
            # Генерация изображения (например, 500x500 пикселей, красный фон)
            with Image.new("RGB", (500, 500), color="red") as img:
                img.save(image_bytes, format="PNG")
                image_bytes.seek(0)  # Перемещаем указатель в начало

            payload = MultipartEncoder(
                fields={
                    "taskID": f"{task_id}",
                    "CompletedWorkID": f"{completed_work_id}",
                    "IsPublic": "false",
                    "IsIgnorePossibleDuplication": "true",
                    'File': (file_name, image_bytes, 'image/png')
                }
            )
            start = time.time()
            response = requests.post(
                url=self.endpoints.post_upload_file_to_completed_work_from_form_endpoint,
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
            assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}'
            model = CompletedWorkAttachmentsModel(**response.json())
            logger.info(f'Successfully upload {file_name} to completed work with ID: {completed_work_id}, '
                        f'data from form.')
            return model

    @allure.step("Uploads the file to server and binds it to the completed work, data from body.")
    def post_upload_bind_attachment_to_completed_work_data_from_body(self, task_id: int, completed_work_id: int):
        file_name = f'attachment_from_body{randint(1, 999)}.png'
        with io.BytesIO() as image_bytes:
            # Генерация изображения (например, 500x500 пикселей, черный фон)
            with Image.new("RGB", (500, 500), color="black") as img:
                img.save(image_bytes, format="PNG")
                image_bytes.seek(0)  # Перемещаем указатель в начало
                # Преобразование изображения в строку Base64
                image_base64 = base64.b64encode(image_bytes.read()).decode('utf-8')

            payload = {
                "taskID": task_id,
                "completedWorkID": completed_work_id,
                "FileName": file_name,
                "ContentType": "image/png",
                "Description": "Файл из тела запроса загружен авто тестом",
                "isPublic": False,
                "IsIgnorePossibleDuplication": True,
                "File": image_base64
            }
            start = time.time()
            response = requests.post(
                url=self.endpoints.post_upload_file_to_completed_work_from_body_endpoint,
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
            model = CompletedWorkAttachmentsModel(**response.json())
            logger.info(f'Successfully upload {file_name} to completed work with ID: {completed_work_id}, '
                        f'data from body.')
            return model
