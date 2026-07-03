import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.msg.msg_triggers.payloads import Payloads
from services.msg.msg_triggers.endpoints import Endpoints
from config.headers import Headers
from services.msg.msg_triggers.models.msg_triggers_model import *
from http import HTTPStatus
import time
from utils.token_utils import get_token


class MsgTriggersAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()
    
    @allure.step("Put update triggers.")
    def put_update_triggers(
        self, 
        trigger_id: int,
        description: str,
        event_id: int,
        template_id: int
        ):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_triggers_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_triggers_payload(
                trigger_id, description, event_id, template_id
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
        logger.success(f'Successfully update triggers.')
        return None
    
    @allure.step("Post add trigger.")
    def post_trigger(
        self, 
        event_id: int,
        template_id: int
        ):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_triggers_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_triggers_payload(
                event_id, template_id
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
        model = SuccessAddTriggersModel(results=response.json())
        logger.success(f'Successfully add trigger with id {model.results[0]}.')
        return model
    
    @allure.step("Delete trigger by ID.")
    def delete_trigger_by_id(
        self, 
        trigger_id: int
        ):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_trigger_endpoint(trigger_id),
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
        logger.success(f'Successfully delete trigger with id {trigger_id}.')
        return None
