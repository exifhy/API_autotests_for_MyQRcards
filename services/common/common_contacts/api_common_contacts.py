from requests import JSONDecodeError
import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.common.common_contacts.payloads import Payloads
from services.common.common_contacts.endpoints import Endpoints
from config.headers import Headers
from services.common.common_contacts.models.common_contacts_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token
from src.generators.generators import generated_user
from random import randint


class CommonContactsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()
        self.contact = next(generated_user())

    @allure.step("Add contacts.")
    def post_add_contacts(self):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_contacts_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_contacts(
                full_name=f'{self.contact.surname} {self.contact.name}',
                email=self.contact.email,
                phone=self.contact.phone,
                desc=f'Создан авто-тестом',
                position=f'Директор{randint(1, 99)}'
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
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}, {response.json()}'
        model = SuccessAddContactModel(contact=response.json())
        logger.info(f'Successfully add contact.')
        return model

    @allure.step("Update contacts.")
    def put_update_contacts(self, contact_id: int):
        new_name = f'Новое имя{randint(1, 99)}'
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_contacts_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_contacts(
                contact_id=contact_id,
                full_name=new_name,
                email=self.contact.email,
                phone=self.contact.phone,
                desc=f'Изменен авто-тестом',
                position=f'Охрана{randint(1, 99)}'
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
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully update contacts.')

    @allure.step("Delete contact by ID.")
    def delete_contact_by_id(self, contact_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_contact_by_id(contact_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected {HTTPStatus.ACCEPTED}, but got {response.status_code}. Message {data_response}'
        logger.warning(f'Successfully delete contact by ID: {contact_id}.')

    @allure.step("Delete list of contacts.")
    def delete_mass_contacts(self, *args):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_contacts_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_mass_of_contact_payload(*args)
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
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.warning(f'Successfully delete contacts with ID: {args}.')

    @allure.step("Get list data contacts.")
    def get_list_contacts(self):
        # params = {
        #     "Range": "items=0-10",
        #     "offset": "10",
        #     "fetch": "10",
        #     "isDeleted": True,
        #     "contactID": int
        # }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_info_contacts_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            f'Status code {response.status_code}, {response.json()}'
        model = SuccessGetListContactsModel(root=response.json())
        logger.info(f'Successfully get list data contacts.')
        return model

    @allure.step("Get data contact by ID.")
    def get_data_contact_by_id(self, contact_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_info_contact_by_id(contact_id),
            headers=self.headers.basic_header(get_token())
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
        model = ContactModel(**response.json())
        logger.info(f'Successfully get data contact by ID: {contact_id}.')
        return model
