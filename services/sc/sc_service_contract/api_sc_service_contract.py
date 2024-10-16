from requests import JSONDecodeError
import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.sc.sc_service_contract.payloads import Payloads
from services.sc.sc_service_contract.endpoints import Endpoints
from config.headers import Headers
from services.sc.sc_service_contract.models.sc_service_contract_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from src.generators.generators import generator_contract

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class ScServiceContractAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()
        self.contract = next(generator_contract())

    @allure.step("Method for creating or updating service contract(s).")
    def post_updates_info_about_custom_object_attributes(self, company_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_method_for_add_contract_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_method_for_add_contract_payload(
                company_id=company_id,
                contract_name=self.contract.name,
                date_from=self.contract.date_from,
                desc=self.contract.description,
                conditions=self.contract.conditions
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
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}, {response.json()}'
        model = SuccessAddServiceContractModel(contract=response.json())
        logger.info(f'Successfully creating or updating service contract(s).')
        return model

    @allure.step("Method for deleting a contract by ID.")
    def delete_contract_by_id(self, contract_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_contract_by_id_endpoint(contract_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully deleting a contract by ID.')

    @allure.step("Method for mass deletion of contracts.")
    def delete_mass_of_contract(self, *args):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_mass_of_contract_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_mass_of_contract_payload(*args)
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
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully mass deleting a contract.')

    @allure.step("Add a list of objects to the contract.")
    def post_add_list_object_to_contract(self, contract_id: int, asset_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_list_object_to_contract_endpoint(contract_id),
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_add_list_object_to_contract_payload(
                asset_id=asset_id,
                child=True
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
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}, {response.json()}'
        model = SuccessContractAssetAddProjectionModel(**response.json())
        logger.info(f'Successfully add a list of objects to the contract.')
        return model

    @allure.step("Method for updating service contract(s).")
    def put_update_method_for_exist_contract(self, contract_id: int, company_id: int):
        new_contract_name = self.contract.name
        new_date_yesterday = self.contract.date_from
        new_desc = self.contract.description
        new_conditions = self.contract.conditions
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_method_for_exist_contract_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.put_method_for_update_contract_payload(
                contract_id=contract_id,
                company_id=company_id,
                contract_name=new_contract_name,
                date_from=new_date_yesterday,
                desc=new_desc,
                conditions=new_conditions
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
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully updating service contract(s).')
        return new_contract_name, new_date_yesterday, new_desc, new_conditions

    @allure.step("Method of get service contract by ID.")
    def get_contract_by_id(self, contract_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_method_of_contract_by_id_endpoint(contract_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, f'Status code {response.status_code}, {response.json()}'
        model = SuccessGetContractResultModel(**response.json())
        logger.info(f'Successfully add a list of objects to the contract.')
        return model

    @allure.step("Method of get mass service contract by ID.")
    def get_mass_contract_by_id(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_method_list_of_contract_endpoint,
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.PARTIAL_CONTENT, HTTPStatus.OK}, \
            f'Status code {response.status_code}, {response.json()}'
        model = SuccessGetMassContractDictModel(root=response.json())
        logger.info(f'Successfully get mass service contract by ID.')
        return model

    @allure.step("Method of get the list of service contract objects.")
    def get_list_of_contract_objects(self, contract_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_of_contract_objects_endpoint(contract_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.PARTIAL_CONTENT, HTTPStatus.OK}, \
            f'Status code {response.status_code}, {response.json()}'
        model = SuccessGetListContractObjectsModel(root=response.json())
        logger.info(f'Successfully get the list of service contract objects.')
        return model

    @allure.step("Method of get the total number of service contracts.")
    def head_method_total_count_of_contract(self):
        start = time.time()
        response = requests.head(
            url=self.endpoints.head_method_total_count_of_contract_endpoint,
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully get the total number of service contracts.')
