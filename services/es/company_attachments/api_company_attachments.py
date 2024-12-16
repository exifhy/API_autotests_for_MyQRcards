import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.es.company_attachments.payloads import Payloads
from services.es.company_attachments.endpoints import Endpoints
from config.headers import Headers
from services.es.company_attachments.models.company_attachments_model import *
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


class EsCompanyAttachmentsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Binds the company and the attachments.")
    def post_bind_attachments_and_company(self, company_id: int, *attachment_ids: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_bind_attachments_and_company_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_bind_attachments_and_company_payload(
                company_id,
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
        model = SuccessBindAttachmentsAndCompanyModel(result=response.json())
        logger.info(
            f'Successfully bind attachments ID: {attachment_ids} and company with ID: {company_id}.')
        return model

    @allure.step("Unbind company and attachments.")
    def delete_unbind_attachments_and_company(self, company_id: int, *attachment_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_unbind_attachments_and_company_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_unbind_attachments_from_company_payload(
                company_id,
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
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Code:{response.status_code}.Message:{response.json()}'
        logger.warning(
            f'Successfully unbind attachments ID: {attachment_ids} and company with ID: {company_id}.')

    @allure.step("Uploads the file to a file server and binds it to the company, data from form.")
    def post_upload_and_bind_to_company_data_from_form(self, company_id: int):
        file_name = f'attachment_from_form{randint(1, 999)}.png'
        with io.BytesIO() as image_bytes:
            # Генерация изображения (например, 500x500 пикселей, красный фон)
            with Image.new("RGB", (500, 500), color="red") as img:
                img.save(image_bytes, format="PNG")
                image_bytes.seek(0)  # Перемещаем указатель в начало

            payload = MultipartEncoder(
                fields={
                    "companyID": f"{company_id}",
                    "IsPublic": "false",
                    "IsIgnorePossibleDuplication": "true",
                    'File': (file_name, image_bytes, 'image/png')
                }
            )
            start = time.time()
            response = requests.post(
                url=self.endpoints.post_upload_attachments_to_company_data_from_form_endpoint,
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
            model = SuccessUploadCompanyAttachmentsModel(**response.json())
            logger.info(f'Successfully upload {file_name} to company with ID: {company_id}, data from form.')
            return model

    @allure.step("Uploads the file to a file server and binds it to the company, data from body.")
    def post_upload_bind_attachment_to_company_data_from_body(self, company_id: int):
        file_name = f'attachment_from_body{randint(1, 999)}.png'
        with io.BytesIO() as image_bytes:
            # Генерация изображения (например, 500x500 пикселей, черный фон)
            with Image.new("RGB", (500, 500), color="black") as img:
                img.save(image_bytes, format="PNG")
                image_bytes.seek(0)  # Перемещаем указатель в начало
                # Преобразование изображения в строку Base64
                image_base64 = base64.b64encode(image_bytes.read()).decode('utf-8')

            payload = {
                "companyID": company_id,
                "FileName": file_name,
                "ContentType": "image/png",
                "Description": "Файл из тела запроса загружен авто тестом",
                "isPublic": False,
                "IsIgnorePossibleDuplication": True,
                "File": image_base64
            }
            start = time.time()
            response = requests.post(
                url=self.endpoints.post_upload_attachments_to_company_data_from_body_endpoint,
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
            model = SuccessUploadCompanyAttachmentsModel(**response.json())
            logger.info(f'Successfully upload {file_name} to company with ID: {company_id}, data from body.')
            return model
