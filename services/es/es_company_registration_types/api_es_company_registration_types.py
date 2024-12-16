import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.es.es_company_registration_types.payloads import Payloads
from services.es.es_company_registration_types.endpoints import Endpoints
from config.headers import Headers
from services.es.es_company_registration_types.models.es_company_registration_types_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


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
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, f'{response.json()}, {response.status_code}'
        model = SuccessGetCompanyRegistrationTypesModel(root=response.json())
        logger.info(f'Successfully get company registration types.')
        return model
