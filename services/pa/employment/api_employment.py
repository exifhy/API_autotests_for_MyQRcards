import allure
import requests
from loguru import logger
from datetime import datetime
from utils.helper import Helper
from services.pa.employment.payloads import Payloads
from services.pa.employment.endpoints import Endpoints
from config.headers import Headers
from services.pa.employment.models.employment_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class PaEmploymentAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add employment to user.")
    def post_add_user_employment_by_id(self, user_id, customer_org_unit_id):
        date = datetime.now()
        start = time.time()
        response = requests.post(
            url=self.endpoints.add_employment_to_user_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.add_employment_customers_payload(
                user_id,
                customer_org_unit_id,
                date.strftime("%Y-%m-%d")
            )
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessEmploymentAdd(list=response.json())
        logger.info(f'Successfully add employment to user.')
        return model
