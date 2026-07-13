import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.msg.msg_message_templates.payloads import Payloads
from services.msg.msg_message_templates.endpoints import Endpoints
from config.headers import Headers
from services.msg.msg_message_templates.models.msg_message_templates_model import *
from http import HTTPStatus
import time
from utils.token_utils import get_token


class MsgMessageTemplatesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()
    
    @allure.step("Put update message templates, create new task, provider email.")
    def put_update_message_templates_email_create_task(
        self, 
        msg_template_id: int,
        provider_id: int
        ):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_message_templates_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_message_templates_create_task_payload(
                msg_template_id, provider_id
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
        logger.success(f'Successfully update message templates, create new task, provider email.')
        return None
    
    @allure.step("Put update message template.")
    def put_update_message_template(
        self, 
        msg_template_id: int,
        description_template: str,
        subject_template: str,
        content_template: str,
        provider_id: int
        ):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_message_templates_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_message_template_payload(
                msg_template_id, 
                description_template,
                subject_template,
                content_template,
                provider_id
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
        logger.success(f'Successfully update message template with ID {msg_template_id}.')
        return None
    
    @allure.step("Put validate message templates.")
    def put_validate_message_templates(self, template_id: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_validate_message_template_endpoint(template_id),
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
        logger.success(f'Successfully validate message templates.')
        return None
    
    @allure.step("Post add message templates.")
    def post_add_message_template(self, subject_template: str, content_template: str, provider_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_message_templates_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_message_templates_payload(
                subject_template, content_template, provider_id
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
        model = SuccessAddMessageTemplatesModel(results=response.json())
        logger.success(f'Successfully add message template with ID {model.results[0]}.')
        return model
    
    @allure.step("Delete message templates by id.")
    def delete_message_templates_by_id(self, msg_template_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_message_template_endpoint(msg_template_id),
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
        logger.success(f'Successfully delete message templates with id {msg_template_id}.')
        return None
    
    @allure.step("Get mass message templates.")
    def get_message_templates(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_message_templates_list_endpoint,
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
        model = SuccessMessageTemplatesModel(root=response.json())
        logger.success(f'Successfully get message templates.')
        return model
    
    @allure.step("Get message template by ID.")
    def get_message_template_by_id(self, template_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_message_template_endpoint(template_id),
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
        model = GetMessageTemplatesModel(**response.json())
        logger.success(f'Successfully get message template by ID {template_id}.')
        return model
