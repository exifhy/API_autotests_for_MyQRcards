import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.common.common_attributes.payloads import Payloads
from services.common.common_attributes.endpoints import Endpoints
from config.headers import Headers
from services.common.common_attributes.models.common_attributes_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token
from dotenv import load_dotenv
import os
from random import randint

load_dotenv()
APP_ID = os.getenv('APP_ID')


class CommonAttributesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Attribute creation method for contract only.")
    def post_add_method_attributes_only_for_contract(self):
        """
        Attribute type ID
        1. Строка
        2. Целое число
        3. Дробное число
        4. Дата
        5. Дата и время
        6. Значение из списка
        7. Множественный выбор из списка
        8. Многострочный текст
        9. Переключатель
        10. Вложенный файл
        11. Редактируемый рисунок
        """
        attribute_name = f'Доп поле - {randint(1, 999)}'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_method_attributes_endpoint,
            headers=self.headers.auth_header(bearer_token=get_token(), app_id=APP_ID),
            json=self.payloads.post_add_method_attributes_type_str_payloads(
                attribute_name=attribute_name,
                attribute_type_id=1,
                for_task=False,
                for_asset=False,
                for_check_list=False,
                fro_complete_work=False,
                for_contract=True,
                for_company=False
            )
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessAddAttributeModel(values=response.json())
        logger.info(f'Successfully attribute creation method only for contract with name: {attribute_name}.')
        return model

    @allure.step("Attribute creation method for asset only type string.")
    def post_add_method_attributes_only_for_asset_str(self):
        attribute_name = f'Доп поле - {randint(1, 999)}'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_method_attributes_endpoint,
            headers=self.headers.auth_header(bearer_token=get_token(), app_id=APP_ID),
            json=self.payloads.post_add_method_attributes_type_str_payloads(
                attribute_name=attribute_name,
                attribute_type_id=1,
                for_task=False,
                for_asset=True,
                for_check_list=False,
                fro_complete_work=False,
                for_contract=False,
                for_company=False
            )
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessAddAttributeModel(values=response.json())
        logger.info(f'Successfully attribute type str creation method only for asset with name: {attribute_name}.')
        return model

    @allure.step("Attribute creation method for checklist, type attachment.")
    def post_add_attribute_only_for_checklist_attachment(self):
        attribute_name = f'Поле фото чек-листа - {randint(1, 999)}'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_method_attributes_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_method_attributes_type_str_payloads(
                attribute_name=attribute_name,
                attribute_type_id=10,
                for_task=False,
                for_asset=False,
                for_check_list=True,
                fro_complete_work=False,
                for_contract=False,
                for_company=False
            )
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessAddAttributeModel(values=response.json())
        logger.info(f'Successfully add attribute type attachment only for checklist with name: {attribute_name}.')
        return model

    @allure.step("Attribute creation method for customer.")
    def post_add_attribute_only_for_customer(self):
        attribute_name = f'Поле для заказчика - {randint(1, 999)}'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_method_attributes_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_attribute_to_user_payloads(
                attribute_name=attribute_name,
                attribute_type_id=randint(1, 11),
                customer=True,
                stuff=False
            )
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code{HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessAddAttributeModel(values=response.json())
        logger.info(f'Successfully add attribute type 2 only for customer with name: {attribute_name}.')
        return model

    @allure.step("Attribute creation method for stuff.")
    def post_add_attribute_only_for_stuff(self):
        attribute_name = f'Поле для сотрудника - {randint(1, 999)}'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_method_attributes_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_attribute_to_user_payloads(
                attribute_name=attribute_name,
                attribute_type_id=randint(1, 11),
                customer=False,
                stuff=True
            )
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code{HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessAddAttributeModel(values=response.json())
        logger.info(f'Successfully add attribute type 2 only for stuff with name: {attribute_name}.')
        return model

    @allure.step("Attribute creation method for stuff and customer.")
    def post_add_attribute_for_stuff_and_customer(self):
        attribute_name = f'Поле для сотрудника и заказчика - {randint(1, 999)}'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_method_attributes_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_attribute_to_user_payloads(
                attribute_name=attribute_name,
                attribute_type_id=randint(1, 11),
                customer=True,
                stuff=True
            )
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code{HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessAddAttributeModel(values=response.json())
        logger.info(f'Successfully add attribute type 2 only for stuff and customer with name: {attribute_name}.')
        return model

    @allure.step("Attribute creation method stuff false and customer false.")
    def post_add_attribute_stuff_and_customer_false(self):
        attribute_name = f'Поле бзе привязки - {randint(1, 999)}'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_method_attributes_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_attribute_to_user_payloads(
                attribute_name=attribute_name,
                attribute_type_id=randint(1, 11),
                customer=False,
                stuff=False
            )
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code{HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessAddAttributeModel(values=response.json())
        logger.info(f'Successfully add attribute type 2 stuff and customer false with name: {attribute_name}.')
        return model

    @allure.step("Attribute creation method for complete work, type attachment.")
    def post_add_attribute_only_for_complete_work_attachment(self):
        attribute_name = f'Поле фото выполненной работы - {randint(1, 999)}'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_method_attributes_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_method_attributes_type_str_payloads(
                attribute_name=attribute_name,
                attribute_type_id=10,
                for_task=False,
                for_asset=False,
                for_check_list=False,
                fro_complete_work=True,
                for_contract=False,
                for_company=False
            )
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code{HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessAddAttributeModel(values=response.json())
        logger.info(f'Successfully add attribute type attachment only for complete work with name: {attribute_name}.')
        return model

    @allure.step("Attribute creation method for complete work, type string.")
    def post_add_attribute_only_for_complete_work_string(self):
        attribute_name = f'Поле строка выполненной работы - {randint(1, 999)}'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_method_attributes_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_method_attributes_type_str_payloads(
                attribute_name=attribute_name,
                attribute_type_id=1,
                for_task=False,
                for_asset=False,
                for_check_list=False,
                fro_complete_work=True,
                for_contract=False,
                for_company=False
            )
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code{HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessAddAttributeModel(values=response.json())
        logger.info(f'Successfully add attribute type string only for complete work with name: {attribute_name}.')
        return model

    @allure.step("Attribute creation method for task only type string.")
    def post_add_method_attributes_only_for_task_str(self):
        attribute_name = f'Доп поле строка для заявки - {randint(1, 999)}'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_method_attributes_endpoint,
            headers=self.headers.auth_header(bearer_token=get_token(), app_id=APP_ID),
            json=self.payloads.post_add_method_attributes_type_str_payloads(
                attribute_name=attribute_name,
                attribute_type_id=1,
                for_task=True,
                for_asset=False,
                for_check_list=False,
                fro_complete_work=False,
                for_contract=False,
                for_company=False
            )
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessAddAttributeModel(values=response.json())
        logger.info(f'Successfully attribute type str creation method only for task with name: {attribute_name}.')
        return model

    @allure.step("Attribute creation method for company only type string.")
    def post_add_method_attributes_only_for_company_str(self):
        attribute_name = f'Доп поле для компании - {randint(1, 999)}'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_method_attributes_endpoint,
            headers=self.headers.auth_header(bearer_token=get_token(), app_id=APP_ID),
            json=self.payloads.post_add_method_attributes_type_str_payloads(
                attribute_name=attribute_name,
                attribute_type_id=1,
                for_task=False,
                for_asset=False,
                for_check_list=False,
                fro_complete_work=False,
                for_contract=False,
                for_company=True
            )
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessAddAttributeModel(values=response.json())
        logger.info(f'Successfully attribute type str creation method only for company with name: {attribute_name}.')
        return model

    @allure.step("Attribute creation method for all relevant essence with type -Value from list-.")
    def post_add_method_attributes_only_for_all_relevant_essence_with_type_6(self):
        """
        Attribute type ID
        6 Значение из списка
        """
        attribute_name = f'Доп поле - {randint(1, 999)}'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_method_attributes_endpoint,
            headers=self.headers.auth_header(bearer_token=get_token(), app_id=APP_ID),
            json=self.payloads.post_add_method_attributes_type_str_payloads(
                attribute_name=attribute_name,
                attribute_type_id=6,
                for_task=True,
                for_asset=True,
                for_check_list=True,
                fro_complete_work=True,
                for_contract=True,
                for_company=True
            )
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessAddAttributeModel(values=response.json())
        logger.warning(
            f'Successfully attribute creation method for all relevant essence with type '
            f'-Value from list- with name: {attribute_name}.')
        return model

    @allure.step("Attribute deletion method by ID.")
    def delete_method_attribute_by_id(self, attribute_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_method_attribute_by_id_endpoint(attribute_id),
            headers=self.headers.auth_header(bearer_token=get_token(), app_id=APP_ID)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.warning(f'Successfully delete attribute by ID: {attribute_id}.')

    @allure.step("Get list attributes.")
    def get_list_attributes(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_attributes_endpoint,
            headers=self.headers.auth_header(bearer_token=get_token(), app_id=APP_ID)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT},'
             f'but got {response.status_code}, {data_response}')
        model = SuccessGetAttributesModel(root=response.json())
        logger.warning(f'Successfully get list attributes.')
        return model

    @allure.step("Get list attributes and return id attribute 'Attachment' for checklist.")
    def get_list_attributes_return_id_attribute_attachment_for_checklist(self):
        param = {
            "isDeleted": False
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_attributes_endpoint, params=param,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessGetAttributesModel(root=response.json())
        attachment_attribute_id = None
        for key, value in model.root.items():
            if value.type and value.relevantFor:
                if value.type.code == "Attachment" and value.type.id == 10 and value.relevantFor.checkList:
                    attachment_attribute_id = int(key)
                    logger.warning(f'Successfully get list attributes and return id {attachment_attribute_id} '
                                   f'attribute "Attachment" for checklist.')
                    break
        if attachment_attribute_id:
            return attachment_attribute_id
        else:
            model = self.post_add_attribute_only_for_checklist_attachment()
            return model.values[0]

    @allure.step("Get list attributes and return id attribute 'Attachment' for complete work.")
    def get_list_attributes_return_id_attribute_attachment_for_complete_work(self):
        param = {
            "isDeleted": False
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_attributes_endpoint, params=param,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessGetAttributesModel(root=response.json())
        attachment_attribute_id = None
        for key, value in model.root.items():
            if value.type and value.relevantFor:
                if value.type.code == "Attachment" and value.type.id == 10 and value.relevantFor.completedWork:
                    attachment_attribute_id = int(key)
                    logger.warning(f'Successfully get list attributes and return id {attachment_attribute_id} '
                                   f'attribute "Attachment" for complete work.')
                    break
        if attachment_attribute_id:
            return attachment_attribute_id
        else:
            model = self.post_add_attribute_only_for_complete_work_attachment()
            return model.values[0]

    @allure.step("Get attribute by ID.")
    def get_attribute_by_id(self, attribute_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_attribute_by_id_endpoint(attribute_id),
            headers=self.headers.auth_header(bearer_token=get_token(), app_id=APP_ID)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}, {data_response}')
        model = AttributeResultList(**response.json())
        logger.warning(f'Successfully get attribute by ID.')
        return model

    @allure.step("Delete mass attributes by list.")
    def delete_attributes_by_list(self, *attribute_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_mass_attributes_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_method_attribute_payload(*attribute_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.warning(f'Successfully mass delete attributes method by list.')

    @allure.step("Get available values for an attribute.")
    def get_available_values_for_attribute(self, attribute_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_available_values_for_attribute_endpoint(attribute_id),
            headers=self.headers.auth_header(bearer_token=get_token(), app_id=APP_ID)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.error(f'Status code: {response.status_code}, NO CONTENT.')
            return None

        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT},'
             f'but got {response.status_code}, {data_response}')
        model = SuccessAvailableValuesForAttributeModel(**response.json())
        logger.warning(f'Successfully get available values for an attribute by ID.')
        return model, response.json()
