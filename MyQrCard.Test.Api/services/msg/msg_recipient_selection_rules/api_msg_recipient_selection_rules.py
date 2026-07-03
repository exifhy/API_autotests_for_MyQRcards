import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.msg.msg_recipient_selection_rules.payloads import Payloads
from services.msg.msg_recipient_selection_rules.endpoints import Endpoints
from config.headers import Headers
from services.msg.msg_recipient_selection_rules.models.msg_recipient_selection_rules_model import *
from http import HTTPStatus
import time
from utils.token_utils import get_token


class MsgRecipientSelectionRulesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()
    
    @allure.step("Put update recipient selection rules.")
    def put_update_recipient_selection_rules(
        self, 
        recipient_id: int,
        custom_role_id: int
        ):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_recipient_selection_rules_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_recipient_selection_rules_payload(
                recipient_id, custom_role_id
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
        logger.success(f'Successfully update recipient selection rules.')
        return None
    
    @allure.step("Post add recipient selection rules.")
    def post_recipient_selection_rules(
        self, 
        custom_role_id: int
        ):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_recipient_selection_rules_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_recipient_selection_rules_payload(
                custom_role_id
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
        model = SuccessAddRecipientSelectionRulesModel(results=response.json())
        logger.success(f'Successfully add recipient selection rules.')
        return model
    
    @allure.step("Delete recipient selection rules.")
    def delete_recipient_selection_rules(
        self, 
        rule_id: int
        ):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_recipient_selection_rule_endpoint(rule_id),
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
        logger.success(f'Successfully delete recipient selection rule by id {rule_id}.')
        return None
