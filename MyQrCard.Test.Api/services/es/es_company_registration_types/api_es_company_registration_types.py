import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.es.es_company_registration_types.payloads import Payloads
from services.es.es_company_registration_types.endpoints import Endpoints
from config.headers import Headers
from services.es.es_company_registration_types.models.es_company_registration_types_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class EsCompanyRegistrationTypesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get company registration types.")
    def get_company_registration_types(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_company_registration_types_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.json()}, {data_response}'
        model = SuccessGetCompanyRegistrationTypesModel(root=response.json())
        logger.info(f'Successfully get company registration types.')
        return model
