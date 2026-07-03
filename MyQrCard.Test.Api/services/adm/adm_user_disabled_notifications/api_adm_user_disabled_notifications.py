import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.adm.adm_user_disabled_notifications.payloads import Payloads
from services.adm.adm_user_disabled_notifications.endpoints import Endpoints
from config.headers import Headers
from services.adm.adm_user_disabled_notifications.models.adm_user_disabled_notifications_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class AdmUserDisabledNotificationsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("User disabled notifications.")
    def post_user_disabled_notifications(self, user_id: int, model_user):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_user_disabled_notifications_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_user_disabled_notifications_payload(
                user_id, model_user.providers[0].id, False
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
            (f'Expected status code {HTTPStatus.ACCEPTED}, '
             f'but got {response.status_code}, {data_response}')
        model = UserDisabledNotificationsListResponseModel(results=response.json())
        logger.info(f'Successfully add user ID {user_id} disabled notifications.')
        return model
