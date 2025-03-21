import random
import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.work.work_task_templates.payloads import Payloads
from services.work.work_task_templates.endpoints import Endpoints
from config.headers import Headers
from services.work.work_task_templates.models.work_task_templates_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class WorkTaskTemplatesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add task templates.")
    def post_add_task_templates(self, asset_id: int, task_type_id: str, work_type_id: str):
        name = f"Шаблон заявки - {random.randint(1, 999)}"
        note = "Создана авто-тестом"
        start = time.time()
        response = requests.post(
            url=self.endpoints.add_task_templates_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.add_task_templates_payloads(
                template_name=name,
                templates_note=note,
                asset_id=asset_id,
                task_type_id=task_type_id,
                work_type_id=work_type_id
            )
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}, {response.json()}'
        model = SuccessAddTaskTemplatesModel(templates=response.json())
        logger.info(f'Successfully created task templates with id: {model.templates[0]} ')
        return model

    @allure.step("Update task templates.")
    def put_update_task_templates(self, template_id: str, asset_id: int, task_type_id: str, work_type_id: str):
        model_task_template_before = self.get_list_task_templates()
        code_str = model_task_template_before.root[template_id].code
        name = f"Измененный шаблон заявки - {random.randint(1000, 9999)}"
        note = "Изменен авто-тестом"
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_task_templates_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.put_update_task_templates_payloads(
                template_id=template_id,
                template_name=name,
                templates_note=note,
                asset_id=asset_id,
                task_type_id=task_type_id,
                work_type_id=work_type_id,
                code_str=code_str
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
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        model_task_template_after = self.get_list_task_templates()
        assert model_task_template_before.root[template_id] != model_task_template_after.root[template_id], \
            f'Task template has not been updated.'
        logger.info(f'Successfully update task template with id: {template_id}.')

    @allure.step("Returns a list of task templates by ID.")
    def get_list_task_templates_by_id(self, task_templates_id: str):
        params = {
            "taskTemplateID": task_templates_id
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_task_templates_endpoint, params=params,
            headers=self.headers.basic_header(API_TOKEN),
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            f'Status code {response.status_code}, {response.json()}'
        model = SuccessGetTaskTemplatesModel(**response.json())
        logger.info(f'Successfully received list task templates with id: {model.root[task_templates_id].id}')
        logger.info(f'Successfully received list task templates with name: {model.root[task_templates_id].name}')
        logger.info(f'Successfully received list task templates with notes: {model.root[task_templates_id].notes}')
        return model

    @allure.step("Get a list of task templates.")
    def get_list_task_templates(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_task_templates_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
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
        model = SuccessGetTaskTemplatesModel(**response.json())
        logger.info(f'Successfully get list task templates.')
        return model

    @allure.step("Get task template by ID.")
    def get_task_template_by_id(self, task_template_id: str):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_task_template_by_id_endpoint(task_template_id),
            headers=self.headers.basic_header(API_TOKEN),
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
        model = TaskTemplatesGetResultModel(**response.json())
        logger.info(f'Successfully get task template by ID {task_template_id}.')
        return model

    @allure.step("Head task templates.")
    def head_task_templates(self):
        start = time.time()
        response = requests.head(
            url=self.endpoints.head_task_templates_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
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
        logger.info(f'Successfully get head <{response.headers['Content-Range']}> task templates.')

    @allure.step("Get download qr code task templates.")
    def get_download_qr_code_task_templates(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_download_qr_code_task_templates_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info('Tenant does not contain qr code archive.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {response.json()}.'
        assert response.headers["Content-Type"] == "application/zip", "Wrong Content-Type"
        assert "attachment; filename=qrCodes.zip" in response.headers["Content-Disposition"], \
            "Wrong Content-Disposition"
        assert int(response.headers["Content-Length"]) > 0, "Empty archive"
        assert "X-Trace-Identifier" in response.headers, "No header X-Trace-Identifier"
        logger.info(f'Successfully get download qr code task templates.')
        return None

    @allure.step("Get download qr code by task template ID.")
    def get_download_qr_code_task_template_by_id(self, task_template_id: str):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_download_qr_code_task_template_by_id_endpoint(task_template_id),
            headers=self.headers.basic_header(API_TOKEN),
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info('Task template does not contain qr code archive.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {response.json()}.'
        assert response.headers["Content-Type"] == "image/svg+xml", "Wrong Content-Type"
        assert "attachment; filename=qrCode.svg" in response.headers["Content-Disposition"], \
            "Wrong Content-Disposition"
        assert int(response.headers["Content-Length"]) > 0, "Empty body"
        assert "X-Trace-Identifier" in response.headers, "No header X-Trace-Identifier"
        logger.info(f'Successfully get download qr code task template by ID {task_template_id}.')
        return None

    @allure.step("Delete task templates by ID.")
    def delete_task_templates_by_id(self, task_templates_id: str):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_task_templates_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_task_templates_payloads(task_templates_id)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.warning(f'Successfully delete task templates by ID {task_templates_id}.')

    @allure.step("Publishes task template.")
    def put_publish_task_template(self, task_templates_id: str):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_publish_task_template_by_id_endpoint(task_templates_id),
            headers=self.headers.basic_header(API_TOKEN)
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
        model = PublishTaskTemplateModel(**response.json())
        logger.info(f'Successfully publish task template by ID {task_templates_id}.')
        return model

    @allure.step("Unpublishes task template.")
    def put_unpublish_task_template(self, task_templates_id: str):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_unpublish_task_template_by_id_endpoint(task_templates_id),
            headers=self.headers.basic_header(API_TOKEN)
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
        logger.info(f'Successfully unpublish task template by ID {task_templates_id}.')

    @allure.step("Get public task template.")
    def get_public_task_template(self, task_templates_id: str):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_public_task_template_by_id_endpoint(task_templates_id),
            headers=self.headers.basic_header(API_TOKEN)
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
        model = GetPublicResultModel(**response.json())
        logger.info(f'Successfully get public task template by ID {task_templates_id}.')
        return model

    @allure.step("Binds employee to the task template by list.")
    def post_bind_employee_to_template_by_list(self, task_templates_id: str, *user_ids: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_assignment_task_templates_endpoint(task_templates_id),
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.bind_employee_to_template_payloads(*user_ids)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}, {response.json()}'
        model = SuccessTaskTemplateAssignmentMergeModel(task=response.json())
        logger.info(f'Successfully binds employee to the template by ID.')
        return model

    @allure.step("Get list employee from task template by ID.")
    def get_list_users_from_task_template_by_id(self, task_templates_id: str):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_assignment_task_templates_endpoint(task_templates_id),
            headers=self.headers.basic_header(API_TOKEN)
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
        model = SuccessGetListTaskTemplateAssignmentDetailsProjectionModel(results=response.json())
        logger.info(f'Successfully get list users from task template by ID.')
        return model

    @allure.step("Add task template for the schedule.")
    def post_add_task_templates_for_schedules_by_id(self, task_templates_id: str, schedule_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_task_templates_for_schedules_endpoint(task_templates_id),
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.add_task_templates_for_schedules_payloads(schedule_id)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully add task template to schedule.')

    @allure.step("Get list excluded assets from task template.")
    def get_list_excluded_assets_from_task_template(self, task_templates_id: str):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_excluded_assets_task_templates_endpoint(task_templates_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info("Task template does not contain excluded assets")
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessGetListExcludedAssetsTaskTemplateModel(root=response.json())
        logger.info(f'Successfully get list excluded assets from task template by ID {task_templates_id}.')
        return model

    @allure.step("Delete excluded assets from task template by asset ID.")
    def delete_excluded_assets_from_task_template_by_asset_id(self, task_templates_id: str, asset_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_excluded_assets_task_templates_by_asset_id_endpoint(task_templates_id, asset_id),
            headers=self.headers.basic_header(API_TOKEN)
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
        logger.warning(f'Successfully delete excluded assets ID {asset_id} from task template by ID {task_templates_id}.')

    @allure.step("Regeneration of events for schedule.")
    def post_appointments_schedules_task_templates(self, task_templates_id: str, schedule_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_task_templates_for_schedules_appointments_endpoint(task_templates_id, schedule_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, {response.status_code}, {data_response}'
        logger.info(f'Successfully add appointments to schedule task template.')

    @allure.step("Get list task template schedule.")
    def get_list_task_templates_schedules(self, task_templates_id: str):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_task_templates_for_schedules_endpoint(task_templates_id),
            headers=self.headers.basic_header(API_TOKEN)
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
        model = SuccessGetListGetSchedulesResultModel(results=response.json())
        logger.info(f'Successfully get list task template schedule.')
        return model

    @allure.step("Schedule activation by ID.")
    def put_schedule_activation_by_id(self, task_templates_id: str, schedule_id: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.activate_schedule_endpoint(task_templates_id, schedule_id),
            headers=self.headers.basic_header(API_TOKEN),
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        model = SuccessActivateTaskTemplatesSchedulesModel(**response.json())
        assert model.isActive is True, f'Expected True, but got {model.isActive}'
        logger.info(f'Successfully schedule activation by ID.')
        return model

    @allure.step("Schedule deactivation by ID.")
    def put_schedule_deactivation_by_id(self, task_templates_id: str, schedule_id: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.deactivate_schedule_endpoint(task_templates_id, schedule_id),
            headers=self.headers.basic_header(API_TOKEN),
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully schedule deactivation by ID.')

