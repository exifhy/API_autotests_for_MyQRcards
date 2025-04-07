from requests import JSONDecodeError
import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.work.work_task_attachments.payloads import Payloads
from services.work.work_task_attachments.endpoints import Endpoints
from config.headers import Headers
from services.work.work_task_attachments.models.work_task_attachments_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token
from random import randint
from requests_toolbelt import MultipartEncoder
from PIL import Image
import io
import base64


class WorkTaskAttachmentsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Adds a uploaded attachments file to a task.")
    def post_task_attachments(self, task_id: int, *attachment_ids: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_bind_attachments_to_task_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_bind_attachments_to_task_payload(
                task_id,
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
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}, {response.json()}'
        model = SuccessTaskAttachmentsModel(result=response.json())
        logger.info(f'Successfully adds a uploaded attachments with ID: {attachment_ids}'
                    f' file to a task with ID: {task_id}.')
        return model

    @allure.step("Delete a uploaded attachments file from task.")
    def delete_task_attachments(self, task_id: int, *attachment_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_unbind_attachments_from_task_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_unbind_attachments_from_task_payload(
                task_id,
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
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.warning(f'Successfully delete uploaded attachments file with ID: {attachment_ids}'
                       f' from task with ID: {task_id}.')

    @allure.step("Uploads the file to server and binds it to the task, data from form.")
    def post_upload_attachment_and_bind_to_task_data_from_form(self, task_id: int):
        file_name = f'attachment_from_form{randint(1, 999)}.png'
        with io.BytesIO() as image_bytes:
            # Генерация изображения (например, 500x500 пикселей, зеленый фон)
            with Image.new("RGB", (500, 500), color="green") as img:
                img.save(image_bytes, format="PNG")
                image_bytes.seek(0)  # Перемещаем указатель в начало

            payload = MultipartEncoder(
                fields={
                    "taskID": f"{task_id}",
                    "IsPublic": "false",
                    "IsIgnorePossibleDuplication": "true",
                    'File': (file_name, image_bytes, 'image/png')
                }
            )
            start = time.time()
            response = requests.post(
                url=self.endpoints.post_upload_attachments_to_task_from_form_endpoint,
                headers=self.headers.upload_file_header(get_token(), payload.content_type),
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
            model = TaskAttachmentsModel(**response.json())
            logger.info(f'Successfully upload {file_name} to task with ID: {task_id}, data from form.')
            return model

    @allure.step("Uploads the file to server and binds it to the task, data from body.")
    def post_upload_bind_attachment_to_task_data_from_body(self, task_id: int):
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
                "FileName": file_name,
                "ContentType": "image/png",
                "Description": "Файл из тела запроса загружен авто тестом",
                "isPublic": False,
                "IsIgnorePossibleDuplication": True,
                "File": image_base64
            }
            start = time.time()
            response = requests.post(
                url=self.endpoints.post_upload_attachments_to_task_from_body_endpoint,
                headers=self.headers.basic_header(get_token()),
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
            model = TaskAttachmentsModel(**response.json())
            logger.info(f'Successfully upload {file_name} to task with ID: {task_id}, data from body.')
            return model
