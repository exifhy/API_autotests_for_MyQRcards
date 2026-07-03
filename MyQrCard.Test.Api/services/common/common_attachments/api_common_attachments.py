import base64
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
from utils.token_utils import get_token


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
                headers=self.headers.upload_file_header(get_token(), payload.content_type),
                data=payload
            )
            end = time.time()
            logger.info(response.headers)
            self.attach_response_headers(response.headers)
            data_response = self.response_content(response)
            self.attach_response(data_response)
            self.attach_time(start, end)
            self.attach_url(response.request.url)
            assert response.status_code == HTTPStatus.CREATED, \
                f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}. {data_response}'
            model = SuccessUploadAttachmentsToServerDataFromFormModel(**response.json())
            logger.info(f'Successfully upload file - {file_name} to server.')
            return model

    @allure.step("Upload files (many) to server V2, data from form.")
    def post_upload_attachments_to_server_data_from_form_v2(self):

        file_name = f'generated_image{randint(600, 699)}.png'
        file_name_second = f'generated_image{randint(999, 9999)}.jpg'

        image_bytes = io.BytesIO()
        with Image.new("RGB", (100, 100), color="green") as img:
            img.save(image_bytes, format="PNG")
        image_bytes.seek(0)

        image_bytes_second = io.BytesIO()
        with Image.new("RGB", (100, 100), color="red") as img2:
            img2.save(image_bytes_second, format="JPEG")
        image_bytes_second.seek(0)

        payload = MultipartEncoder(
            fields={
                "Attachments[0].IsPublic": "false",
                "Attachments[0].IsIgnorePossibleDuplication": "true",
                'Attachments[0].File': (file_name, image_bytes, 'image/png'),
                "Attachments[1].IsPublic": "false",
                "Attachments[1].IsIgnorePossibleDuplication": "true",
                'Attachments[1].File': (file_name_second, image_bytes_second, 'image/jpeg'),
            }
        )
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_upload_attachments_to_server_from_form_v2_endpoint,
            headers=self.headers.upload_file_header(get_token(), payload.content_type),
            data=payload
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}. {data_response}'
        model = SuccessUploadAttachmentsToServerDataFromFormV2Model(results=response.json())
        logger.info(f'Successfully upload files - {file_name, file_name_second} to server.')
        return model

    @allure.step("Upload the file to server, data from body.")
    def post_upload_attachment_data_from_body(self):
        file_name = f'attachment_from_body{randint(999, 9999)}.png'
        with io.BytesIO() as image_bytes:
            with Image.new("RGB", (500, 500), color="black") as img:
                img.save(image_bytes, format="PNG")
                image_bytes.seek(0)
                image_base64 = base64.b64encode(image_bytes.read()).decode('utf-8')

            payload = {
                "FileName": file_name,
                "ContentType": "image/png",
                "Description": "Файл из тела запроса загружен авто тестом",
                "isPublic": False,
                "IsIgnorePossibleDuplication": True,
                "File": image_base64
            }
            start = time.time()
            response = requests.post(
                url=self.endpoints.post_upload_attachments_to_server_from_body_endpoint,
                headers=self.headers.basic_header(get_token()),
                json=payload
            )
            end = time.time()
            logger.info(response.headers)
            self.attach_response_headers(response.headers)
            data_response = self.response_content(response)
            self.attach_response(data_response)
            self.attach_time(start, end)
            self.attach_url(response.request.url)
            assert response.status_code == HTTPStatus.CREATED, \
                f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}. {data_response}'
            model = SuccessUploadAttachmentsToServerDataFromFormModel(**response.json())
            logger.info(f'Successfully upload {file_name} to server, data from body. ID {model.attachmentID}.')
            return model

    @allure.step("Delete attachment by ID.")
    def delete_attachment_by_id(self, attachment_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_attachment_endpoint(attachment_id),
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
        logger.warning(f'Successfully delete attachment by ID: {attachment_id}.')

    @allure.step("Delete attachments by list.")
    def delete_attachments_by_list(self, *attachment_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_attachments_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_attachments_by_list_payload(*attachment_ids)
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
        logger.warning(f'Successfully delete attachments by list: {attachment_ids}.')

    @allure.step("Get download attachment (noRedirect=true).")
    def get_download_attachment_no_redirect_true(self, attachment_id: int):
        param = {
            "noRedirect": True
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_attachments_link_endpoint(attachment_id), params=param,
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
        model = SuccessGetAttachmentModel(**response.json())
        logger.info(f'Successfully get attachment noRedirect=true: {attachment_id}.')
        return model

    @allure.step("Get TemporaryRedirect to a temporary link for downloading the attachment.")
    def get_downloading_attachment(self, model_attachment):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_attachments_link_endpoint(model_attachment.attachmentID),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}.'
        assert response.content, "Response content is empty, expected file data"
        assert response.headers.get("Content-Type") is not None, "Content-Type header is missing"
        assert "application/octet-stream" in response.headers["Content-Type"] or "application/" in response.headers[
            "Content-Type"], \
            f"Unexpected Content-Type: {response.headers['Content-Type']}"
        assert f'filename="{model_attachment.fileName}"' in response.headers["Content-Disposition"], \
            f"Unexpected Content-Disposition: {response.headers['Content-Disposition']}"
        logger.info(f'Successfully get TemporaryRedirect to a temporary link to download a file.')

    @allure.step("Get list attachments for current user.")
    def get_list_attachments_for_current_user(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_attachments_endpoint,
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
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list of attachments available to the user.")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}, {data_response}')
        model = SuccessGetAttachmentsListResultModel(root=response.json())
        logger.info(f'Successfully get list attachments for current user. Quantity {len(model.root)}.')
        return model

    @allure.step("Get list attachments for current user by attachmentID.")
    def get_list_attachments_for_current_user_by_attachment_id(self, attach_id: int):
        param = {
            "attachmentID": attach_id
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_attachments_endpoint, params=param,
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
        model = SuccessGetAttachmentsListResultModel(root=response.json())
        assert model.root[str(attach_id)], f"Invalid attachment returned"
        assert len(model.root) == 1, "More than one attachment returned"
        logger.info(f'Successfully get list attachments for current user by ID {attach_id}. Qty {len(model.root)}.')
        return model

    def get_list_attachments_for_current_user_deleted(self, deleted: bool):
        with allure.step(f"Get list attachments for current user. isDeleted={deleted}."):
            param = {
                "isDeleted": deleted
            }
            start = time.time()
            response = requests.get(
                url=self.endpoints.get_list_attachments_endpoint, params=param,
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
                logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list of attachments available to the user.")
                return None
            assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
                (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
                 f'but got {response.status_code}, {data_response}')
            model = SuccessGetAttachmentsListResultModel(root=response.json())
            logger.info(f'Successfully get list attachments for current user, isDeleted={deleted}.')
            return model

    @allure.step("Get attachment data by ID.")
    def get_attachment_data_by_id(self, model_attach):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_attachment_data_by_id_endpoint(model_attach.attachmentID),
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
        model = AttachmentsListResultModel(**response.json())
        assert model.id == model_attach.attachmentID, f"Expected {model.id}, but got {model_attach.attachmentID}."
        assert model.fileName == model_attach.fileName, f"Expected {model.fileName}, but got {model_attach.fileName}."
        logger.info(f'Successfully get attachment data by ID {model_attach.attachmentID}.')
        return model

    @allure.step("Publish attachment by ID.")
    def post_publish_attachment_by_id(self, attach_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_attachment_publish_endpoint(attach_id),
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
        model = PublishAttachmentModel(**response.json())
        logger.info(f'Successfully publish attachment by ID {attach_id}.')
        return model

    @allure.step("Unpublish attachment by ID.")
    def post_unpublish_attachment_by_id(self, attach_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_attachment_unpublish_endpoint(attach_id),
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
        logger.info(f'Successfully unpublish attachment by ID {attach_id}.')
        return None

    @allure.step("Get attachment download link for task.")
    def get_attachment_download_link_for_task(self, task_id: int):
        param = {
            "taskID": task_id
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_download_link_attachments_endpoint, params=param,
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
        model = DownloadLinkResultModel(**response.json())
        logger.info(f'Successfully get attachment download link for task.')
        return model
