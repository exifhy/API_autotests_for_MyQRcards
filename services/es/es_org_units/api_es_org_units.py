import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.es.es_org_units.payloads import Payloads
from services.es.es_org_units.endpoints import Endpoints
from config.headers import Headers
from services.es.es_org_units.models.es_org_units_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class EsOrgUnitsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get root org units.")
    def get_root_org_units(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_org_units_root_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, f'{response.status_code}, {response.json()}'
        model = SuccessGetListOrgUnitsModel(root=response.json())
        logger.info(f'Successfully get root orgunits.')
        return model

    @allure.step("Get root org units by company ID.")
    def get_root_org_units_by_company_id(self, company_id: int):
        params = {
            "companyID": company_id
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_org_units_root_endpoint, params=params,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, f'{response.status_code}, {response.json()}'
        model = SuccessGetListOrgUnitsModel(root=response.json())
        logger.info(f'Successfully get root org units by company ID.')
        return model

    @allure.step("Get org units by company ID.")
    def get_org_units_by_company_id(self, company_id: int):
        params = {
            "companyID": company_id
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_org_units_endpoint, params=params,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, f'{response.status_code}, {response.json()}'
        model = SuccessGetListOrgUnitsModel(root=response.json())
        logger.info(f'Successfully get org units by company ID.')
        return model

    @allure.step("Get org units.")
    def get_org_units(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_org_units_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, f'{response.status_code}, {response.json()}'
        model = SuccessGetListOrgUnitsModel(root=response.json())
        logger.info(f'Successfully get org units.')
        return model

    @allure.step("Get org units by ID.")
    def get_org_units_by_id(self, unit_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_org_units_by_id_endpoint(unit_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning(f"Status code: {response.status_code}, NO CONTENT.")
        else:
            assert response.status_code == HTTPStatus.OK, f'{response.status_code}, {response.json()}'
            model = SuccessGetListOrgUnitsModel(root=response.json())
            logger.info(f'Successfully get org units by id.')
            return model
