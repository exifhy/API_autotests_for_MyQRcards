import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.ui.ui_layout_templates.payloads import Payloads
from services.ui.ui_layout_templates.endpoints import Endpoints
from config.headers import Headers
from services.ui.ui_layout_templates.models.ui_layout_templates_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class UILayoutTemplatesAPI(Helper):
    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get list task layout templates.")
    def get_list_task_layout_templates(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_layout_templates_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning('NO CONTENT (204)')
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}, {data_response}')
        model = LayoutTemplateDtoListModel(result=response.json())
        logger.info(f'Successfully get list task layout templates.')
        return model

    @allure.step("Get list task layout templates with taskTypeID.")
    def get_list_task_layout_templates_with_task_type_id(self, task_type_id: int):
        param = {
            "taskTypeID": task_type_id
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_layout_templates_endpoint, params=param,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning('NO CONTENT (204)')
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}, {data_response}')
        model = LayoutTemplateDtoListModel(result=response.json())
        logger.info(f'Successfully get list task layout templates with taskTypeID.')
        return model

    @allure.step("Get list task layout templates with isDefault.")
    def get_list_task_layout_templates_with_is_default(self, status: bool):
        param = {
            "isDefault": status
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_layout_templates_endpoint, params=param,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning('NO CONTENT (204)')
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}, {data_response}')
        model = LayoutTemplateDtoListModel(result=response.json())
        logger.info(f'Successfully get list task layout templates with isDefault.')
        return model

    @allure.step("Create a default layout template.")
    def post_default_layout_template(self):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_default_template_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.CONFLICT:
            logger.warning('Default layout template has been created')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = LayoutTemplateDtoModel(**response.json())
        logger.info(f'Successfully create a default layout template.')
        return model

    @allure.step("Resets the layout template settings to the default template state.")
    def put_reset_layout_template_to_default_state(self, template_id: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_reset_template_to_default_condition_endpoint(template_id),
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
        model = LayoutTemplateDtoModel(**response.json())
        logger.info(f'Successfully create a default layout template.')
        return model

    @allure.step("Create layout template.")
    def post_add_layout_template(self):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_create_template_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads
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
        model = LayoutTemplateDtoModel(**response.json())
        logger.info(f'Successfully create layout template.')
        return model

    @allure.step("Get task layout template by id.")
    def get_task_layout_template_by_id(self, template_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_template_by_id_endpoint(template_id),
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
        model = LayoutTemplateDtoModel(**response.json())
        logger.info(f'Successfully get task layout template by ID {template_id}.')
        return model

    @allure.step("Get deleted task layout template by id.")
    def get_deleted_task_layout_template_by_id(self, template_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_template_by_id_endpoint(template_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            f'Expected status code {HTTPStatus.NOT_FOUND}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_data_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Get nonexistent task layout template by id.")
    def get_nonexistent_task_layout_template_by_id(self, template_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_template_by_id_endpoint(template_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            f'Expected status code {HTTPStatus.NOT_FOUND}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_data_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Update layout template.")
    def put_update_layout_template(self, template_id: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_template_endpoint(template_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads
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
        model = LayoutTemplateDtoModel(**response.json())
        logger.info(f'Successfully create layout template.')
        return model

    @allure.step("Delete layout template by ID.")
    def delete_layout_template(self, template_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_template_by_id_endpoint(template_id),
            headers=self.headers.basic_header(get_token()),
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
        logger.warning(f'Successfully delete layout template by ID {template_id}.')

    @allure.step("Get layout template by type by ID.")
    def get_layout_template_by_type_by_id(self, template_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_templates_by_type_endpoint(template_id),
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
        model = LayoutTemplateDtoModel(**response.json())
        logger.info(f'Successfully get layout template by type by ID {template_id}.')
        return model

    @allure.step("Get task type layout template by ID.")
    def get_task_type_layout_template_by_id(self, template_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_task_types_layout_template_by_id_endpoint(template_id),
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
        model = LayoutTaskTypeDtoModel(**response.json())
        logger.info(f'Successfully get task type layout template by ID {template_id}.')
        return model

    @allure.step("Add task types to layout template.")
    def put_add_task_types_to_layout_template(self, template_id: int, *task_types_ids: int or tuple):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_set_task_types_to_layout_template_by_id_endpoint(template_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_add_task_types_to_layout_template_payload(*task_types_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.info(f'Successfully add task types to layout template.')

    @allure.step("Delete task types from layout template.")
    def delete_task_types_from_layout_template(self, template_id: int, *task_types_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.put_set_task_types_to_layout_template_by_id_endpoint(template_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_task_types_from_layout_template_payload(*task_types_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.info(f'Successfully delete task types from layout template.')

    @allure.step("Get list components layout template by ID.")
    def get_list_components_layout_template_by_id(self, template_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_components_layout_templates_endpoint(template_id),
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
        model = ComponentDtoListModel(result=response.json())
        logger.info(f'Successfully get list components layout template by ID {template_id}.')
        return model

    @allure.step("Get list attributes layout template by ID.")
    def get_list_attributes_layout_template_by_id(self, template_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_components_layout_templates_endpoint(template_id),
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
        model = AttributeDtoListModel(result=response.json())
        logger.info(f'Successfully get list attributes layout template by ID {template_id}.')
        return model
