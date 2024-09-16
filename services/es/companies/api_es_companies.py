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
from src.generators.generators import generator_company

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class EsCompaniesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()
        self.company = next(generator_company())

    @allure.step("Add a our company.")
    def post_add_our_company(self):
        name_new_company = self.company.name
        start = time.time()
        response = requests.post(
            url=self.endpoints.add_company_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.add_companies_payload(
                name=name_new_company,
                type_id=3,
                company_our=True,
                company_employer=False,
                company_contractor=False
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

    @allure.step("Marks company as remove.")
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

    @allure.step("Returns a list of companies available to the user.")
    def get_list_companies(self):
        # params = {
        #     "searchText": str,
        #     "Range": str,
        #     "offset": str,
        #     "fetch": str,
        #     "isDeleted": bool,
        #     "taskTypeID": int,
        #     "companyID": int,
        #     "companyRegistrationTypeID": int,
        #     "isEmployer": bool,
        #     "isContractorHolder": bool,
        #     "isOurCompany": bool,
        #     "isVATTaxpayer": bool
        # }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_companies_endpoint,
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code in {HTTPStatus.OK,
                                        HTTPStatus.PARTIAL_CONTENT}, f'Status code {response.status_code}'
        logger.info(response.headers)
        self.attach_time(start, end)
        model = SuccessGetCompaniesListResultModel(**response.json())
        logger.info(f'Successfully receiving a list of companies available to the user.')
        return model

    @allure.step("Update company by id.")
    def put_update_company_by_id(
            self,
            company_id: int,
            customer_id: int,
            staff_id: int
    ):
        new_name_company = self.company.name
        new_email_company = self.company.email
        new_phone_company = self.company.phone
        new_type_individual_company = "2"
        start = time.time()
        response = requests.put(
            url=self.endpoints.add_company_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.update_companies_payload(
                company_id=company_id,
                company_name=new_name_company,
                company_email=new_email_company,
                company_contractor=True,
                company_employer=True,
                company_our=False,
                company_phone=new_phone_company,
                company_type=new_type_individual_company,
                customer_id=customer_id,
                staff_id=staff_id
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_request(response.request.body)
        self.attach_time(start, end)
        logger.warning(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}'
        model = self.get_detailed_information_on_company_by_id(company_id)
        assert model.name == new_name_company, f'Expected -> {new_name_company}, but got -> {model.name}'
        assert model.email == new_email_company, f'Expected -> {new_email_company}, but got -> {model.email}'
        assert model.phone == new_phone_company, f'Expected -> {new_phone_company}, but got -> {model.phone}'
        assert model.registrationTypeID == int(new_type_individual_company), \
            f'Expected -> {new_type_individual_company}, but got -> {model.registrationTypeID}'
        assert model.isOurCompany is False, f'Expected -> False, but got -> {model.isOurCompany}'
        assert model.isContractorHolder is True, f'Expected -> False, but got -> {model.isContractorHolder}'
        assert model.isEmployer is True, f'Expected -> True, but got -> {model.isEmployer}'
        logger.info(f'Successfully update company, name: {new_name_company}.')
