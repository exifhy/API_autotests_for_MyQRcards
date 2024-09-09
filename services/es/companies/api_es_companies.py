import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.es.companies.payloads import Payloads
from services.es.companies.endpoints import Endpoints
from config.headers import Headers
from services.es.companies.models.companies_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from faker import Faker

fake_ru = Faker('ru_RU')

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class EsCompaniesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add a our company.")
    def post_add_our_company(self):
        name_new_company = fake_ru.company()
        start = time.time()
        response = requests.post(
            url=self.endpoints.add_company_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.add_companies_payload(
                name=name_new_company,
                type_id=3
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}'
        self.attach_request(response.request.body)
        self.attach_time(start, end)
        model = SuccessAddCompaniesModel(companies=response.json())
        logger.info(f'Successfully created Our company, name: {name_new_company}.')
        return model.companies[0]

    @allure.step("Marks company as remote.")
    def delete_company_by_id(self, company_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_company_by_id_endpoint(company_id),
            headers=self.headers.basic_header(API_TOKEN),
        )
        end = time.time()
        logger.info(response.headers)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}'
        self.attach_time(start, end)
        logger.info(f'Successfully mark company remote, id: {company_id}.')

    @allure.step("Returns the company available to the user by id.")
    def get_detailed_information_on_company_by_id(self, company_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_company_by_id_endpoint(company_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.OK, f'Status code {response.status_code}'
        logger.info(response.headers)
        self.attach_time(start, end)
        model = SuccessCompaniesGetResult(**response.json())
        logger.info(f'Successfully receiving the company detailed info by id.')
        return model
