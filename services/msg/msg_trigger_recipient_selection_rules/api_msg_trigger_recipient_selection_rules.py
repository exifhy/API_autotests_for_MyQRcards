import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.msg.msg_trigger_recipient_selection_rules.payloads import Payloads
from services.msg.msg_trigger_recipient_selection_rules.endpoints import Endpoints
from config.headers import Headers
from services.msg.msg_trigger_recipient_selection_rules.models.msg_trigger_recipient_selection_rules_model import *
from http import HTTPStatus
import time
from utils.token_utils import get_token


class MsgTriggerRecipientSelectionRulesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()
    
    @allure.step("Post add trigger recipient selection rules.")
    def post_trigger_recipient_selection_rules(
        self, 
        trigger_id: int,
        recipient_selection_rule_id: int
        ):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_trigger_recipient_selection_rules_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_trigger_recipient_selection_rules_payload(
                trigger_id, recipient_selection_rule_id
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
        logger.success(f'Successfully add trigger recipient selection rules.')
        return None