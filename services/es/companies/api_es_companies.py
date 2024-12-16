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
from random import randint

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
            url=self.endpoints.post_add_company_endpoint,
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
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, f'{response.status_code}, {response.json()}'
        model = SuccessAddCompaniesModel(companies=response.json())
        logger.info(f'Successfully created Our company, name: {name_new_company}.')
        return model.companies[0]

    @allure.step("Delete company by ID.")
    def delete_company_by_id(self, company_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_company_by_id_endpoint(company_id),
            headers=self.headers.basic_header(API_TOKEN),
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, f'{response.status_code}, {response.json()}'
        logger.warning(f'Successfully delete company, id: {company_id}.')

    @allure.step("Delete companies by list.")
    def delete_companies_by_list(self, *company_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_companies_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_companies_by_list_payload(*company_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, f'{response.status_code}, {response.json()}'
        logger.warning(f'Successfully delete companies by list IDs: {company_ids}.')

    @allure.step("Head companies.")
    def head_companies(self):
        start = time.time()
        response = requests.head(
            url=self.endpoints.head_companies_endpoint,
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            f'{response.status_code}, {response.json()}'
        logger.info(f'Successfully get head companies.')

    @allure.step("Returns the company available to the user by id.")
    def get_detailed_information_on_company_by_id(self, company_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_company_by_id_endpoint(company_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.OK, f'{response.status_code}, {response.json()}'
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
        #     "isDeleted": False,
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
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
        assert response.status_code in {HTTPStatus.OK,
                                        HTTPStatus.PARTIAL_CONTENT}, f'{response.status_code}, {response.json()}'
        model = SuccessGetCompaniesListResultModel(**response.json())
        logger.info(f'Successfully receiving a list of companies available to the user not deleted.')
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
            url=self.endpoints.put_update_company_endpoint,
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
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.ACCEPTED, f'{response.status_code}, {response.json()}'
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

    @allure.step("Returns list company attachments.")
    def get_list_attachments_from_company(self, company_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_attachments_from_company_endpoint(company_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            f'{response.status_code}, {response.json()}'
        model = SuccessGetListAttachmentResultModel(root=response.json())
        logger.info(f'Successfully get attachments from company with iD: {company_id}.')
        return model

    @allure.step("Download attachment from company by ID.")
    def get_download_attachment_from_company(self, company_id: int, attachment_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_download_attachment_from_company_endpoint(company_id, attachment_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Status code {response.status_code}, {response.json()}'
        assert response.content, "Response content is empty, expected file data"
        assert response.headers.get("Content-Type") is not None, "Content-Type header is missing"
        assert "application/octet-stream" in response.headers["Content-Type"] or "application/" in response.headers[
            "Content-Type"], \
            f"Unexpected Content-Type: {response.headers['Content-Type']}"
        logger.info(f'Successfully get download attachment {attachment_id} from company by id: {company_id}.')

    @allure.step("Get info attachment file from company by ID.")
    def get_attachment_info_from_company(self, company_id: int, attachment_id):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_info_attachment_from_company_by_id_endpoint(company_id, attachment_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.OK, \
            f'{response.status_code}, {response.json()}'
        model = SuccessGetAttachmentResultModel(**response.json())
        logger.info(f'Successfully get info attachment file from company by ID: {company_id}.')
        return model

    @allure.step("Get info attributes from company by ID.")
    def get_attributes_info_from_company(self, company_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_attributes_from_company_endpoint(company_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.OK, \
            f'{response.status_code}, {response.json()}'
        model = SuccessGetListCompanyAttributeResultModel(result=response.json())
        logger.info(f'Successfully get info attributes from company by ID: {company_id}.')
        return model

    @allure.step("Update company attributes by ID.")
    def post_update_company_attributes(self, company_id: int, attribute_id: int):
        params = {
            "attributeID": str(attribute_id),
            "values": [
                f"Значение доп поля {randint(1, 9999)}"
            ],
            "isPublic": False
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_attributes_to_company_endpoint(company_id),
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_add_attributes_to_company_payload(*params)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'{response.status_code}, {response.json()}'
        logger.info(f'Successfully bind attributes to company by ID: {company_id}.')

    @allure.step("Get company bank accounts by ID.")
    def get_bank_accounts_from_company(self, company_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_bank_accounts_from_company_endpoint(company_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            f'{response.status_code}, {response.json()}'
        model = SuccessGetCompanyBankAccountListResultModel(root=response.json())
        logger.info(f'Successfully get company bank accounts by ID: {company_id}.')
        return model

    @allure.step("Update company bank accounts by ID.")
    def put_update_company_bank_accounts(
            self,
            company_id: int,
            bank_id: int,
            company_bank_account_id: int,
    ):
        params = {
            "bankID": bank_id,
            "companyBankAccountID": company_bank_account_id,
            "checkingAccount": f"{randint(10000000000000000000, 99999999999999999999)}",
        }
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_bank_accounts_by_company_endpoint(company_id),
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.put_update_bank_accounts_by_company_payload(params)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'{response.status_code}, {response.json()}'
        logger.info(f'Successfully update company bank accounts by ID: {company_id}.')

    @allure.step("Add bank accounts to company by ID.")
    def post_add_bank_accounts_to_company(
            self,
            company_id: int,
            bank_id: int,
    ):
        params = {
            "bankID": bank_id,
            "checkingAccount": f"{randint(10000000000000000000, 99999999999999999999)}"
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_bank_accounts_to_company_endpoint(company_id),
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_add_bank_accounts_to_company_payload(params)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.CREATED, \
            f'{response.status_code}, {response.json()}'
        model = SuccessAddBakAccountsToCompanyModel(result=response.json())
        logger.info(f'Successfully add bank accounts to company by ID: {company_id}.')
        return model

    @allure.step("Delete bank accounts from company by list.")
    def delete_bank_accounts_from_company_by_list(self, company_id: int, *bank_account_company_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_bank_accounts_from_company_by_list_endpoint(company_id),
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_bank_accounts_from_company_by_list_payload(*bank_account_company_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'{response.status_code}, {response.json()}'
        logger.warning(f'Successfully delete bank accounts from company by list: {bank_account_company_ids}.')

    @allure.step("Delete bank account from company by ID.")
    def delete_bank_account_from_company_by_id(self, company_id: int, bank_account_company_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_bank_account_from_company_by_id_endpoint(company_id, bank_account_company_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'{response.status_code}, {response.json()}'
        logger.warning(f'Successfully delete bank accounts from company by ID: {bank_account_company_id}.')

    @allure.step("Get list company contacts.")
    def get_list_contacts_from_company(self, company_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_contacts_from_company_endpoint(company_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            f'{response.status_code}, {response.json()}'
        model = SuccessGetListCompanyContactsResultModel(root=response.json())
        logger.info(f'Successfully get list company contacts by ID: {company_id}.')
        return model

    @allure.step("Get company contact by ID.")
    def get_contact_from_company_by_id(self, company_id: int, contact_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_contact_from_company_by_id_endpoint(company_id, contact_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.OK, \
            f'{response.status_code}, {response.json()}'
        model = CompanyContactsResultModel(**response.json())
        logger.info(f'Successfully get company contact by ID: {contact_id}.')
        return model

    @allure.step("Add contact to company by ID.")
    def post_add_contact_to_company_by_id(self, company_id: int, contact_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_contact_to_company_by_id_endpoint(company_id, contact_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.CREATED, \
            f'{response.status_code}, {response.json()}'
        model = SuccessAddListContactsToCompanyModel(result=response.json())
        logger.info(f'Successfully add contact to company by ID: {contact_id}.')
        return model

    @allure.step("Delete contact from company by ID.")
    def delete_contact_from_company_by_id(self, company_id: int, contact_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_contact_from_company_by_id_endpoint(company_id, contact_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'{response.status_code}, {response.json()}'
        logger.warning(f'Successfully delete contact from company by ID: {contact_id}.')

    @allure.step("Add contacts to company by list.")
    def post_add_contacts_to_company_by_list(self, company_id: int, *contact_ids: int):
        params = {
            "companyID": company_id,
            "data": [
                *contact_ids
            ]
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_contacts_to_company_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_add_contacts_to_company_payload(params)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.CREATED, \
            f'{response.status_code}, {response.json()}'
        model = SuccessAddListContactsToCompanyModel(result=response.json())
        logger.info(f'Successfully add contact to company by list: {contact_ids}.')
        return model

    @allure.step("Delete contacts from company by list.")
    def delete_contacts_from_company_by_list(self, company_id: int, *contact_ids: int):
        params = {
            "companyID": company_id,
            "data": [
                *contact_ids
            ]
        }
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_contacts_from_company_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_contacts_from_company_by_list_payload(params)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'{response.status_code}, {response.json()}'
        logger.warning(f'Successfully delete contacts from company by list: {contact_ids}.')

    @allure.step("Restore companies by list.")
    def put_restore_companies_by_list(self, *company_ids: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_restore_companies_by_list_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.put_restore_companies_by_list_payload(*company_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'{response.status_code}, {response.json()}'
        logger.info(f'Successfully restore companies by list: {company_ids}.')

    @allure.step("Find dadata company.")
    def get_find_dadata_company(self, inn: int):
        params = {
            "inn": inn
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_dadata_find_company_endpoint, params=params,
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.OK, \
            f'{response.status_code}, {response.json()}'
        model = SuccessGetCompanyDataModel(**response.json())
        logger.info(f'Successfully get find dadata with inn: {inn}.')
        return model

    @allure.step("Get actual company location.")
    def get_actual_company_location(self, company_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_actual_locations_from_company(company_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning(f"{response.status_code}. No content")
        else:
            assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
                f'{response.status_code}, {response.json()}'
            model = LocationResult(**response.json())
            logger.info(f'Successfully get actual company location with ID: {company_id}.')
            return model
