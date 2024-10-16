from urllib import parse
from typing import List
import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.adm.user_roles.payloads import Payloads
from services.adm.user_roles.endpoints import Endpoints
from config.headers import Headers
from services.adm.user_roles.models.user_roles_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class AdmUserRolesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add roles to a user.")
    def post_add_roles_to_user(self, user_id: int, customer_role_id: List[int]):
        start = time.time()
        response = requests.post(
            url=self.endpoints.add_roles_to_user_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.add_roles_to_user_payload(
                user_id=user_id,
                role_ids=customer_role_id
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, f'{response.status_code}, {response.json()}'
        logger.info(f'Successfully add a roles to user.')
