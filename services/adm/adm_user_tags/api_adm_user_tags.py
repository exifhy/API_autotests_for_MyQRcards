import random
import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.adm.adm_user_tags.payloads import Payloads
from services.adm.adm_user_tags.endpoints import Endpoints
from config.headers import Headers
from services.adm.adm_user_tags.models.adm_user_tags_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class AdmUserTagsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add tags to user.")
    def post_add_tags_to_user(self, user_id: int):
        tag = f"tags-{random.randint(1, 999)}"
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_user_tags_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_user_tags_payload(tag, user_id)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response_headers(response.headers)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = UserTagsListResponseModel(results=response.json())
        logger.info(f'Successfully add tags with ID {tag} to user ID {user_id}.')
        return model

    @allure.step("Delete tags from user.")
    def delete_tags_from_user(self, user_id: int, *tags: str or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_user_tags_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_user_tags_payload(user_id, *tags)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response_headers(response.headers)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.warning(f'Successfully delete tags {tags} from user ID {user_id}.')
        return None
