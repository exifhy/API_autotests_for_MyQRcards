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
            logger.warning("Status code 204")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}, {data_response}')
        model = LayoutTemplateDtoListModel(result=response.json())
        logger.info(f'Successfully get list task layout templates with taskTypeID.')
        return model

    @allure.step("Return list task layout templates with taskTypeID.")
    def return_list_task_layout_templates_with_task_type_id(self, task_type_id: int):
        model_template = self.get_list_task_layout_templates_with_task_type_id(task_type_id)
        if model_template is None:
            model_new_template = self.post_add_layout_template(False, task_type_id)
            self.get_list_task_layout_templates_with_task_type_id(task_type_id)
            self.delete_layout_template_by_id(model_new_template.id)

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
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = LayoutTemplateDtoListModel(result=response.json())
        logger.info(f'Successfully get list task layout templates with isDefault.')
        return model

    @allure.step("Create a default layout template. Default layout template not exists")
    def post_default_layout_template_non_existent(self):
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
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = LayoutTemplateDtoModel(**response.json())
        logger.info(f'Successfully create a default layout template.')
        return model

    @allure.step("Create a default layout template. Default layout template already exists.")
    def post_default_layout_template_already_exists(self):
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
        assert response.status_code == HTTPStatus.CONFLICT, \
            f'Expected status code {HTTPStatus.CONFLICT}, but got {response.status_code}, {data_response}'
        logger.info(f'Default layout template already exists.')
        return None

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
        logger.info(f'Successfully resets the layout template settings to the default template state.')
        return model

    @allure.step("Reset of invalid layout template settings to the default template state.")
    def put_reset_of_invalid_layout_template_to_default_state(self, template_id: int):
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
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            f'Expected status code {HTTPStatus.NOT_FOUND}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_data_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Resets default layout template settings to the default template state.")
    def put_reset_default_layout_template_to_default_state(self):
        model_default_template = self.get_list_task_layout_templates_with_is_default(True)
        if model_default_template is None:
            model_before_default_template = self.post_default_layout_template_non_existent()
            self.put_reset_layout_template_to_default_state(model_before_default_template.id)
            model_after_default_template = self.get_list_task_layout_templates_with_is_default(True)
            assert model_before_default_template == model_after_default_template.result[0], \
                'Default layout template has changed after reset.'
        else:
            self.put_reset_layout_template_to_default_state(model_default_template.result[0].id)
            model_after_default_template = self.get_list_task_layout_templates_with_is_default(True)
            assert model_default_template == model_after_default_template, \
                'Default layout template has changed after reset.'

    @allure.step("Create layout template.")
    def post_add_layout_template(self, default: bool, task_type: int or None):
        name = 'Шаблон создан авто-тестом'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_create_template_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_layout_template_payload(default, name, task_type)
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

    @allure.step("Create layout template without fields.")
    def post_add_layout_template_without_fields(self, default: bool):
        name = 'Шаблон создан авто-тестом'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_create_template_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_layout_template_without_fields_payload(default, name)
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

    @allure.step("Create layout template with deleted taskTypeID.")
    def post_add_layout_template_with_deleted_task_type(self, default: bool, task_type: int or None):
        name = 'Шаблон создан авто-тестом'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_create_template_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_layout_template_payload(default, name, task_type)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CONFLICT, \
            (f'Expected status code {HTTPStatus.CONFLICT}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].code == "TaskTypeDeleted", \
            f'Expected TaskTypeDeleted, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "Тип заявки удален", \
            (f'Expected Тип заявки удален, '
             f'but got {model.list_model[0].message}')
        assert "TaskTypeDeleted" in response.headers["X-Application-Errors"], \
            f'Expected TaskTypeDeleted, but got {response.headers["X-Application-Errors"]}'
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Create layout template with nonexistent taskTypeID.")
    def post_add_layout_template_with_nonexistent_task_type(self, default: bool, task_type: int or None):
        name = 'Шаблон создан авто-тестом'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_create_template_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_layout_template_payload(default, name, task_type)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            f'Expected status code {HTTPStatus.NOT_FOUND}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_data_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Post layout template task types is already in use.")
    def post_add_layout_template_task_type_is_already_in_use(self, default: bool, task_type: int or None):
        name = 'Шаблон создан авто-тестом'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_create_template_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_layout_template_payload(default, name, task_type)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CONFLICT, \
            (f'Expected status code {HTTPStatus.CONFLICT}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].code == "ConflictRequest", \
            f'Expected ConflictRequest, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "Один из типов заявки выбранных для шаблона уже используется", \
            (f'Expected Один из типов заявки выбранных для шаблона уже используется, '
             f'but got {model.list_model[0].message}')
        assert "ConflictRequest" in response.headers["X-Application-Errors"], \
            f'Expected ConflictRequest, but got {response.headers["X-Application-Errors"]}'
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Create layout template task types is already in use.")
    def create_layout_template_task_type_is_already_in_use(self, task_type: int or None):
        model_list_template = self.get_list_task_layout_templates()
        task_type_status = False
        for item in model_list_template.result:
            if len(item.taskTypes) != 0:
                if item.taskTypes[0] == task_type:
                    task_type_status = True
                    break

        if task_type_status is True:
            self.post_add_layout_template_task_type_is_already_in_use(False, task_type)
        else:
            model_template = self.post_add_layout_template(False, task_type)
            self.post_add_layout_template_task_type_is_already_in_use(False, task_type)
            self.delete_layout_template_by_id(model_template.id)

    @allure.step("Create layout template with task types.")
    def create_layout_template_with_task_type(self, task_type: int or None):
        model_list_template = self.get_list_task_layout_templates()
        task_type_status = False
        for item in model_list_template.result:
            if len(item.taskTypes) != 0:
                if item.taskTypes[0] == task_type:
                    task_type_status = True
                    break

        if task_type_status is True:
            self.post_add_layout_template_task_type_is_already_in_use(False, task_type)
        else:
            model_template = self.post_add_layout_template(False, task_type)
            self.post_add_layout_template_task_type_is_already_in_use(False, task_type)
            self.delete_layout_template_by_id(model_template.id)

    @allure.step("Update layout template task types is already in use.")
    def update_layout_template_task_type_is_already_in_use(self, task_type: int or None):
        model_list_template = self.get_list_task_layout_templates()
        task_type_status = False
        for item in model_list_template.result:
            if item.taskTypes and item.taskTypes[0] == task_type:
                task_type_status = True
                break

        if task_type_status:
            model_template = self.post_add_layout_template(False, None)
            self.put_update_layout_template_task_type_is_already_in_use(
                model_template.id, False, task_type
            )
            self.delete_layout_template_by_id(model_template.id)
        else:
            for item in model_list_template.result:
                if not item.taskTypes:
                    self.put_update_layout_template(item.id, False, task_type)
                    self.put_update_layout_template_task_type_is_already_in_use(
                        item.id, False, task_type
                    )
                    self.put_reset_layout_template_to_default_state(item.id)
                    break

    @allure.step("Return layout template task types by template ID.")
    def return_layout_template_task_types_by_template_id(self, task_type: int):
        model_list_template = self.get_list_task_layout_templates()
        task_type_status = False
        template_id = None
        for item in model_list_template.result:
            if item.taskTypes and item.taskTypes[0] == task_type:
                task_type_status = True
                template_id = item.id
                break

        if task_type_status:
            self.get_task_type_layout_template_by_id(template_id)
        else:
            model_template = self.post_add_layout_template(False, task_type)
            self.get_task_type_layout_template_by_id(model_template.id)
            self.delete_layout_template_by_id(model_template.id)

    @allure.step("Get task layout template by ID.")
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

    @allure.step("Get deleted task layout template by ID.")
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

    @allure.step("Get nonexistent task layout template by ID.")
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
    def put_update_layout_template(self, template_id: int, default: bool, task_type: int or None):
        name = 'Обновленный шаблон'
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_template_endpoint(template_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_layout_template_payload(default, name, task_type)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = LayoutTemplateDtoModel(**response.json())
        logger.info(f'Successfully update layout template.')
        return model

    @allure.step("Update deleted layout template.")
    def put_update_deleted_layout_template(self, template_id: int, default: bool, task_type: int or None):
        name = 'Обновленный шаблон'
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_template_endpoint(template_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_layout_template_payload(default, name, task_type)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            f'Expected status code {HTTPStatus.NOT_FOUND}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_data_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("PUT layout template task types is already in use.")
    def put_update_layout_template_task_type_is_already_in_use(
            self, template_id: int, default: bool, task_type: int or None
    ):
        name = 'Обновленный шаблон'
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_template_endpoint(template_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_layout_template_payload(default, name, task_type)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CONFLICT, \
            (f'Expected status code {HTTPStatus.CONFLICT}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].code == "ConflictRequest", \
            f'Expected ConflictRequest, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "Один из типов заявки выбранных для шаблона уже используется", \
            (f'Expected Один из типов заявки выбранных для шаблона уже используется, '
             f'but got {model.list_model[0].message}')
        assert "ConflictRequest" in response.headers["X-Application-Errors"], \
            f'Expected ConflictRequest, but got {response.headers["X-Application-Errors"]}'
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Delete layout template by ID.")
    def delete_layout_template_by_id(self, template_id: int):
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

    @allure.step("Delete invalid layout template by ID.")
    def delete_invalid_layout_template_by_id(self, template_id: int):
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
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            f'Expected status code {HTTPStatus.NOT_FOUND}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_data_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Get layout template by type by ID.")
    def get_layout_template_by_type_by_id(self, task_type_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_templates_by_type_endpoint(task_type_id),
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
        logger.info(f'Successfully get layout template by type by ID {task_type_id}.')
        return model

    @allure.step("Get nonexistent layout template by type by ID.")
    def get_nonexistent_layout_template_by_type_by_id(self, task_type_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_templates_by_type_endpoint(task_type_id),
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

    @allure.step("Get deleted layout template by type by ID.")
    def get_deleted_layout_template_by_type_by_id(self, task_type_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_templates_by_type_endpoint(task_type_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CONFLICT, \
            (f'Expected status code {HTTPStatus.CONFLICT}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].code == "TaskTypeDeleted", \
            f'Expected TaskTypeDeleted, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "Тип заявки удален", \
            f'Expected Тип заявки удален, but got {model.list_model[0].message}'
        assert "TaskTypeDeleted" in response.headers["X-Application-Errors"], \
            f'Expected TaskTypeDeleted, but got {response.headers["X-Application-Errors"]}'
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Get task type layout template by template ID.")
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
        model = ListLayoutTaskTypeDtoModel(results=response.json())
        logger.info(f'Successfully get task type layout template by ID {template_id}.')
        return model

    @allure.step("Get invalid task type layout template by template ID.")
    def get_invalid_task_type_layout_template_by_template_id(self, template_id: int):
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
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            f'Expected status code {HTTPStatus.NOT_FOUND}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_data_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("PUT add task types by list to layout template by ID.")
    def put_add_task_types_by_list_to_layout_template_by_id(
            self, template_id: int, *task_types_ids: int or tuple or None
    ):
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
        logger.info(f'Successfully add task types {task_types_ids} to layout template {template_id}.')

    @allure.step("PUT add task types by list to deleted layout template by ID.")
    def put_add_task_types_by_list_to_deleted_layout_template_by_id(
            self, template_id: int, *task_types_ids: int or tuple
    ):
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
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            f'Expected status code {HTTPStatus.NOT_FOUND}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_data_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Update add task types by list to deleted layout template by ID.")
    def update_add_task_types_by_list_to_deleted_layout_template_by_id(self, task_type: int or None):
        model_list_template = self.get_list_task_layout_templates()
        task_type_status = False
        template_id = None
        for item in model_list_template.result:
            if item.taskTypes and item.taskTypes[0] == task_type:
                task_type_status = True
                template_id = item.id
                break

        if task_type_status:
            logger.warning(f"Found layout template {template_id} with type task {task_type}")
            self.put_add_task_types_by_list_to_layout_template_by_id(template_id, None)

        model_template = self.post_add_layout_template(False, None)
        self.delete_layout_template_by_id(model_template.id)
        self.put_add_task_types_by_list_to_deleted_layout_template_by_id(
            model_template.id, task_type
        )

    @allure.step("PUT add deleted task types by list to layout template by ID.")
    def put_add_deleted_task_types_by_list_to_layout_template_by_id(self, template_id: int, *task_types_ids: int or tuple):
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
        assert response.status_code == HTTPStatus.CONFLICT, \
            (f'Expected status code {HTTPStatus.CONFLICT}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].code == "TaskTypeDeleted", \
            f'Expected TaskTypeDeleted, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "Тип заявки удален", \
            f'Expected Тип заявки удален, but got {model.list_model[0].message}'
        assert "TaskTypeDeleted" in response.headers["X-Application-Errors"], \
            f'Expected TaskTypeDeleted, but got {response.headers["X-Application-Errors"]}'
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("PUT add of the task types is already in use to layout template by ID.")
    def put_add_task_types_is_already_in_use_to_layout_template_by_id(
            self, template_id: int, *task_types_ids: int or tuple
    ):
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
        assert response.status_code == HTTPStatus.CONFLICT, \
            (f'Expected status code {HTTPStatus.CONFLICT}, '
             f'but got {response.status_code}. {data_response}.')
        model = ErrorModel(list_model=response.json())
        assert model.list_model[0].code == "ConflictRequest", \
            f'Expected ConflictRequest, but got {model.list_model[0].code}'
        assert model.list_model[0].message == "Один из типов заявки выбранных для шаблона уже используется", \
            (f'Expected Один из типов заявки выбранных для шаблона уже используется, '
             f'but got {model.list_model[0].message}')
        assert "ConflictRequest" in response.headers["X-Application-Errors"], \
            f'Expected ConflictRequest, but got {response.headers["X-Application-Errors"]}'
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Update add task types by list to layout template by ID.")
    def update_add_task_types_by_list_to_layout_template_by_id(self, task_type: int or None):
        model_list_template = self.get_list_task_layout_templates()
        task_type_status = False
        template_id = None
        for item in model_list_template.result:
            if item.taskTypes and item.taskTypes[0] == task_type:
                task_type_status = True
                template_id = item.id
                break

        if task_type_status:
            self.put_add_task_types_by_list_to_layout_template_by_id(template_id, task_type)
            model_after_template = self.get_task_layout_template_by_id(template_id)
            assert model_after_template.taskTypes[0] == task_type, \
                'Task types was not added to the layout template.'

        else:
            for item in model_list_template.result:
                if not item.taskTypes:
                    self.put_add_task_types_by_list_to_layout_template_by_id(item.id, task_type)
                    model_after_template = self.get_task_layout_template_by_id(item.id)
                    assert model_after_template.taskTypes[0] == task_type, \
                        'Task types was not added to the layout template.'
                    break

    @allure.step("Update add of the task types is already in use to layout template by ID.")
    def update_add_task_types_is_already_in_use_to_layout_template_by_id(self, task_type: int or None):
        model_list_template = self.get_list_task_layout_templates()
        task_type_status = False
        for item in model_list_template.result:
            if item.taskTypes and item.taskTypes[0] == task_type:
                task_type_status = True
                break

        if task_type_status:
            model_template = self.post_add_layout_template_without_fields(False)
            self.put_add_task_types_is_already_in_use_to_layout_template_by_id(
                model_template.id, task_type
            )
            self.delete_layout_template_by_id(model_template.id)

        else:
            for item in model_list_template.result:
                if not item.taskTypes:
                    self.put_add_task_types_by_list_to_layout_template_by_id(item.id, task_type)
                    model_template = self.post_add_layout_template_without_fields(False)
                    self.put_add_task_types_is_already_in_use_to_layout_template_by_id(
                        model_template.id, task_type
                    )
                    self.delete_layout_template_by_id(model_template.id)

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
        model_template = self.get_task_layout_template_by_id(template_id)
        assert not model_template.taskTypes, f'Task type {task_types_ids} not deleted from template {template_id}'
        logger.info(f'Successfully delete task types {task_types_ids} from layout template {template_id}.')

    @allure.step("Delete task types from invalid layout template.")
    def delete_task_types_from_invalid_layout_template(self, template_id: int, *task_types_ids: int or tuple):
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
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            f'Expected status code {HTTPStatus.NOT_FOUND}, but got {response.status_code}, {data_response}'
        model = ErrorModel(list_model=response.json())
        self.assert_data_not_found(response, model)
        logger.warning(f'Expected result: error {response.status_code}, message: {model.list_model[0].message}.')
        return None

    @allure.step("Remove task types from layout template.")
    def remove_task_types_from_layout_template(self, task_type: int or None):
        model_list_template = self.get_list_task_layout_templates()
        task_type_status = False
        template_id = None
        for item in model_list_template.result:
            if item.taskTypes and item.taskTypes[0] == task_type:
                task_type_status = True
                template_id = item.id
                break

        if task_type_status:
            logger.warning(f"Found layout template {template_id} with type task {task_type}")
            self.delete_task_types_from_layout_template(template_id, task_type)

        else:
            for item in model_list_template.result:
                if not item.taskTypes:
                    self.put_add_task_types_by_list_to_layout_template_by_id(item.id, task_type)
                    self.delete_task_types_from_layout_template(item.id, task_type)
                    break

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

    @allure.step("Receive list components layout template by ID.")
    def receive_list_components_layout_template_by_id(self, default: bool):
        model_list_template = self.get_list_task_layout_templates()
        for item in model_list_template.result:
            if item.isDefault is default:
                model_components = self.get_list_components_layout_template_by_id(item.id)
                if default is True:
                    for inuse in model_components.result:
                        assert inuse.isInUse is True, 'Default template contains isInUse: False'
                else:
                    for is_inuse in model_components.result:
                        assert is_inuse.isInUse is False, 'Custom template contains isInUse: True'

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
