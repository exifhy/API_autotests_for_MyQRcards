import random
import allure
import requests
from datetime import timezone, timedelta
import datetime
from loguru import logger
from requests import JSONDecodeError
from requests_toolbelt import MultipartEncoder
from PIL import Image
import io
import base64
from utils.helper import Helper
from services.work.tasks.payloads import Payloads
from services.work.tasks.endpoints import Endpoints
from config.headers import Headers
from services.work.tasks.models.work_tasks_model import *
import time
from http import HTTPStatus
from random import randint
from utils.token_utils import get_token


class WorkTasksAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add task.")
    def post_add_task(self, asset_id: int, company_id: int, work_type_id: str, criticality_id: str, task_type_id: str):
        additional_data = {
            "AssetID": asset_id,
            "WorkTypeID": work_type_id,
            "companyID": company_id
        }
        date = datetime.now(timezone.utc).isoformat(timespec='milliseconds')
        current_time_iso = date.replace('+00:00', 'Z')
        task_number = str(random.randint(9999, 999999999999))
        note_task = f'Заявка создана авто-тестом'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_task_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.add_task_payload(
                criticality_id=criticality_id,
                task_type_id=task_type_id,
                number=task_number,
                note=note_task,
                date=current_time_iso,
                **additional_data
            )
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
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}, {response.json()}'
        model = SuccessAddTasksModel(**response.json())
        logger.info(f'Successfully add a task ID {model.id}')
        return model

    @allure.step("Add task with parent task.")
    def post_add_task_with_parent_task(
            self, asset_id: int, company_id: int, work_type_id: str,
            criticality_id: str, task_type_id: str, parent_id: str
    ):
        additional_data = {
            "AssetID": asset_id,
            "WorkTypeID": work_type_id,
            "companyID": company_id,
            "ParentID": parent_id
        }
        date = datetime.now(timezone.utc).isoformat(timespec='milliseconds')
        current_time_iso = date.replace('+00:00', 'Z')
        task_number = str(random.randint(9999, 999999999999))
        note_task = f'Заявка создана авто-тестом'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_task_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.add_task_payload(
                criticality_id=criticality_id,
                task_type_id=task_type_id,
                number=task_number,
                note=note_task,
                date=current_time_iso,
                **additional_data
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
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessAddTasksModel(**response.json())
        logger.info(f'Successfully add a task ID {model.id} with parent task {parent_id}')
        return model

    @allure.step("Add empty task.")
    def post_add_empty_task(self, task_type_id: str):
        data = {
            "RequestMethodID": 1,
            "TaskTypeID": task_type_id
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_task_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=data
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
        model = SuccessAddTasksModel(**response.json())
        logger.info(f'Successfully add a empty task ID {model.id}')
        return model

    @allure.step("Add empty task without logging.")
    def post_add_empty_task_without_logging(self, task_type_id: str):
        data = {
            "RequestMethodID": 1,
            "TaskTypeID": task_type_id
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_task_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=data
        )
        end = time.time()
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessAddTasksModel(**response.json())
        return model

    @allure.step("Create multiple empty tasks.")
    def post_create_multiple_tasks(self, task_type_id: str, count: int) -> List[int]:
        """
        Создает множество пустых заявок
        :param count: количество созданных заявок
        :param task_type_id: тип заявки строкой
        :return: список заявок
        """
        list_tasks = []

        for i in range(count):
            try:
                model_tasks = self.post_add_empty_task_without_logging(task_type_id)
                list_tasks.append(model_tasks.id)
            except Exception as e:
                logger.error(f"Error creating tasks at iteration {i + 1}: {e}")
                continue

        logger.info(f'Successfully added {len(list_tasks)} tasks out of {count} requested')
        return list_tasks

    @allure.step("Add task with number params.")
    def post_add_task_with_number(
            self,
            asset_id: int,
            company_id: int,
            work_type_id: str,
            criticality_id: str,
            task_type_id: str,
            task_number,
            status_code,
            len_task_number
    ):
        additional_data = {
            "AssetID": asset_id,
            "WorkTypeID": work_type_id,
            "companyID": company_id
        }
        date = datetime.now(timezone.utc).isoformat(timespec='milliseconds')
        current_time_iso = date.replace('+00:00', 'Z')
        note_task = f'Заявка создана авто-тестом'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_task_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.add_task_payload(
                criticality_id=criticality_id,
                task_type_id=task_type_id,
                number=task_number,
                note=note_task,
                date=current_time_iso,
                **additional_data
            )
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response_headers(response.headers)
        self.attach_response(data_response)
        self.attach_request(response.request.body)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == status_code, \
            f'Expected status code {status_code}, but got {response.status_code}, {response.json()}'
        match response.status_code:
            case HTTPStatus.BAD_REQUEST:
                model = ErrorModel(list_model=response.json())
                logger.warning(f'{response.status_code}: {model.list_model[0].message}')
                return None
            case HTTPStatus.CONFLICT:
                model = ErrorModel(list_model=response.json())
                logger.warning(f'{response.status_code}: {model.list_model[0].message}')
                return None
        model = SuccessAddTasksModel(**response.json())
        logger.info(f'Successfully add a task ID {model.id}')
        model_get_task = self.get_detailed_info_task_by_id(model.id)
        assert len(model_get_task.number) == len_task_number, \
            f'Expected {len_task_number}, but got {len(model_get_task.number)}'
        return model

    @allure.step("Update task number.")
    def put_update_task_number(self, task_id: int, task_number: int or str, status_code: int, len_task_number: int):
        date = datetime.now(timezone.utc).isoformat(timespec='milliseconds')
        current_time_iso = date.replace('+00:00', 'Z')
        note_task = 'Заявка изменена авто-тестом'
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_task_by_id_endpoint(task_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_task_payload(
                number=task_number,
                note=note_task,
                date=current_time_iso
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
        assert response.status_code == status_code, \
            f'Expected status code {status_code}, but got {response.status_code}, {data_response}'
        match response.status_code:
            case HTTPStatus.BAD_REQUEST:
                model = ErrorModel(list_model=response.json())
                logger.warning(f'{response.status_code}: {model.list_model[0].message}')
                return None
            case HTTPStatus.CONFLICT:
                model = ErrorModel(list_model=response.json())
                logger.warning(f'{response.status_code}: {model.list_model[0].message}')
                return None
        model_task = self.get_detailed_info_task_by_id(task_id)
        assert len(model_task.number) == len_task_number, \
            f'Expected status code {len_task_number}, but got {len(model_task.number)}'
        logger.info(f'Successfully update task number on the task ID {task_id}.')

    @allure.step("Delete the task by ID.")
    def delete_task_by_id(self, task_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_task_by_id_endpoint(task_id),
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        model = SuccessDeleteTaskModel(list=response.json())
        logger.warning(f'Successfully delete the task with id: {model.list[0].taskID}.')
        return model

    @allure.step("Returns a list of tasks available to the user.")
    def get_list_of_tasks_available_to_user(self):
        params = {
            "fetch": 100,
            "isClosed": False,
            "isDeleted": False,
            "offset": 0,
            "orderBy": 1,
            "sortDirection": 2,
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_task_endpoint, params=params,
            headers=self.headers.basic_header(get_token()),
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
        model = SuccessTaskListResultModel(**response.json())
        logger.info(f'Successfully returns a list of tasks available to the user.')
        return model

    @allure.step("Get list of tasks by taskID.")
    def get_list_of_tasks_by_task_id(self, task_list: List[int]):
        params = {
            "taskID": task_list,
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_task_endpoint, params=params,
            headers=self.headers.basic_header(get_token()),
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
        model = SuccessTaskListResultModel(**response.json())
        logger.info(f'Successfully get a list of tasks by taskID.')
        return model

    @allure.step("Get list tasks return list.")
    def get_list_tasks_list(self):
        list_users = []
        params = {
            "fetch": 100,
            "isClosed": False,
            "isDeleted": False,
            "offset": 0,
            "orderBy": 1,
            "sortDirection": 2,
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_task_endpoint, params=params,
            headers=self.headers.basic_header(get_token()),
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
        model = SuccessTaskListResultModel(**response.json())
        for ids, data in model.root.items():
            int_id = int(ids)
            list_users.append(int_id)
        logger.info(f'Successfully get  list {list_users}.')
        return list_users

    @allure.step("Returns detailed information on the task by id.")
    def get_detailed_info_task_by_id(self, task_id: int):
        # params = {
        #     "taskSnapshotID": int,
        #     "includeSchedule": bool
        # }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_detailed_info_task_by_id_endpoint(task_id),
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response_headers(response.headers)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessDetailedInfoModel(**response.json())
        logger.info(f'Successfully get detailed information on the task ID {task_id}.')
        return model

    @allure.step("Get info task by id.")
    def get_task_by_id(self, task_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_detailed_info_task_by_id_endpoint(task_id),
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        data_response = self.response_content(response)
        self.attach_response_headers(response.headers)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessDetailedInfoModel(**response.json())
        return model

    @allure.step("Check of movement at the task stage.")
    def check_movement_at_the_task_stage(self, list_tasks: List[int], task_stage_id: int, time_sleep: int):
        """
        Проверка перехода заявки на определенную стадию
        :param list_tasks: список tskID, например [1, 2, 3]
        :param task_stage_id: стадия на которую совершается переход
        :param time_sleep: время паузы в секундах зависит от количества заявок, например, 50 заявок 30 секунд.
        :return: None
        """
        failed_tasks = []
        self.sleep_with_progress_bar(time_sleep)
        model_tasks = self.get_list_of_tasks_by_task_id(list_tasks)
        for task_id, task in model_tasks.root.items():
            if task.taskStage.id != task_stage_id:
                failed_tasks.append(task_id)
        if len(failed_tasks) > 0:
            raise AssertionError(f'Tasks {failed_tasks} has not moved to the stage {task_stage_id}')
        logger.info(f'Successfully movement of the task to the stage {task_stage_id}')

    @allure.step("Update task by id.")
    def put_update_task_by_id(self, task_id: int):
        date = datetime.now(timezone.utc).isoformat(timespec='milliseconds')
        current_time_iso = date.replace('+00:00', 'Z')
        task_number = str(random.randint(999, 99999))
        note_task = 'Заявка изменена авто-тестом'
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_task_by_id_endpoint(task_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_task_payload(
                number=task_number,
                note=note_task,
                date=current_time_iso
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
        logger.info(f'Successfully update information on the task by id.')
        return task_number, note_task

    @allure.step("Add conversation to task.")
    def post_add_conversation_to_task(self, task_id: int, external: bool):
        value = f"Сообщение-{randint(1, 999)}"
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_conversation_to_task_endpoint(task_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_conversation_to_task_payload(
                external,
                value
            )
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_request(response.request.body)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessListConversationTaskModel(result=response.json())
        logger.info(f'Successfully add conversation to task with ID: {task_id}.')
        return model

    @allure.step("Add conversation to task from not api user.")
    def post_add_conversation_to_task_from_not_api_user(self, task_id: int, external: bool, token: str):
        value = f"Сообщение-{randint(1, 999)} от Администратора."
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_conversation_to_task_endpoint(task_id),
            headers=self.headers.basic_header(token),
            json=self.payloads.post_add_conversation_to_task_payload(
                external,
                value
            )
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_request(response.request.body)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessListConversationTaskModel(result=response.json())
        logger.info(f'Successfully add conversation to task with ID: {task_id}.')
        return model

    @allure.step("Get task conversation by ID.")
    def get_task_conversation_by_id(self, task_id: int, conversation_id: int, token: str or None, read: bool):
        if token is None:
            token = get_token()
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_conversation_by_id_from_task_endpoint(task_id, conversation_id),
            headers=self.headers.basic_header(token)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = TaskMessageModel(**response.json())
        if read is True:
            assert model.read.byAnyone is True, \
                f'Task conversation ID {conversation_id} is not read.'
            logger.info(f'Task conversation ID {conversation_id} is read.')
        logger.info(f'Successfully get task ID {task_id} conversation with ID: {conversation_id}.')
        return model

    @allure.step("Returns the list of available stages to which the task can be transferred.")
    def get_list_task_stages_next(self, task_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_of_available_stages_to_task_can_transferred_endpoint(task_id),
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = SuccessGetListStagesModel(root=response.json())
        logger.info(f'Successfully get the list of available stages to which the task can be transferred.')
        return model

    @allure.step("Get task assignments history.")
    def get_list_task_assignments(self, task_id: int, model_assignment):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_task_assignments_endpoint(task_id),
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning(f'Successfully get list task assignments, but no content.')
            return None
        else:
            assert response.status_code == HTTPStatus.OK, \
                f'Expected {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
            model = SuccessGetListAssignmentHistoryResultModel(result=response.json())
            assert model.result[0].assignedTo.id == model_assignment.history[0].assignments[0].userID, \
                (f'Expected userID {model.result[0].assignedTo.id},'
                 f' but got {model_assignment.history[0].assignments[0].userID}')
            logger.info(f'Successfully get the list task ID {task_id} assignments.')
            return model

    @allure.step("Get list task attachments.")
    def get_list_task_attachments(self, task_id: int, model_attachment):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_task_attachments_endpoint(task_id),
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning(f'Successfully get list task attachments, but no content.')
            return None
        else:
            assert response.status_code == HTTPStatus.OK, \
                f'Expected {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
            model = SuccessGetListAttachmentResultModel(root=response.json())
            assert str(model_attachment.attachmentID) in model.root, \
                f'Attachment ID{model_attachment.attachmentID} not in list task attachments.'
            assert model_attachment.fileName == model.root[str(model_attachment.attachmentID)].fileName, \
                (f'Expected {model_attachment.fileName}, '
                 f'but got {model.root[str(model_attachment.attachmentID)].fileName}')
            logger.info(f'Successfully get the list task ID {task_id} attachment ID {model_attachment.attachmentID}.')
            return model

    @allure.step("Get task attachment by ID.")
    def get_task_attachment_by_id(self, task_id: int, model_attachment):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_task_attachment_by_id_endpoint(task_id, model_attachment.attachmentID),
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response_headers(response.headers)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = AttachmentResultByIdModel(**response.json())
        assert model_attachment.attachmentID == model.attachmentID, \
            f'Expected attachment ID {model_attachment.attachmentID}, but got {model.attachmentID}.'
        assert model_attachment.fileName == model.fileName, \
            f'Expected {model_attachment.fileName}, but got {model.fileName}'
        logger.info(f'Successfully get task ID {task_id} attachment ID {model_attachment.attachmentID}.')
        return model

    @allure.step("Method to get TemporaryRedirect to a temporary link for downloading the attachment file from task.")
    def get_downloading_attachment_file_from_task(self, task_id: int, model_attachment):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_task_attachments_by_id_temporary_redirect_endpoint(
                task_id,
                model_attachment.attachmentID
            ),
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
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}.'
        assert response.content, "Response content is empty, expected file data"
        assert response.headers.get("Content-Type") is not None, "Content-Type header is missing"
        assert "application/octet-stream" in response.headers["Content-Type"] or "application/" in response.headers[
            "Content-Type"], \
            f"Unexpected Content-Type: {response.headers['Content-Type']}"
        assert f'filename="{model_attachment.fileName}"' in response.headers["Content-Disposition"], \
            f"Unexpected Content-Disposition: {response.headers['Content-Disposition']}"
        logger.info(f'Successfully get TemporaryRedirect to a temporary link to download a file.')

    @allure.step("Get temporary link for downloading the task attachment file. No Redirect.")
    def get_link_task_attachment_no_redirect(self, task_id: int, model_attachment):
        param = {
            "noRedirect": True
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_task_attachments_by_id_temporary_redirect_endpoint(
                task_id,
                model_attachment.attachmentID
            ),
            params=param,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetAttachmentLinkNoRedirectModel(**response.json())
        assert model.fileName == model_attachment.fileName, \
            f'Expected file name {model.fileName}, but got {model_attachment.fileName}'
        logger.info(f'Successfully get temporary link to download a file with ID {model_attachment.attachmentID}.')
        return model

    @allure.step("Get task attributes.")
    def get_task_attributes(self, task_id: int, attribute_id: int, model_attribute):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_task_attributes_endpoint(task_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetListAttributeResultModel(result=response.json())
        for item in model.result:
            if item.attribute and item.attribute.id == attribute_id:
                assert item.attribute.name == model_attribute.name, \
                    f'Expected attribute name {item.attribute.name}, but got {model_attribute.name}.'
        logger.info(f'Successfully get task attribute with ID {attribute_id}.')
        return model

    @allure.step("Get list of logging supported partitions (Tab) and sections of these partitions (Sections).")
    def get_list_task_change_types(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_task_change_types_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetListTaskChangeTypeResultModel(result=response.json())
        logger.info(f'Successfully get list task change types.')
        return model

    @allure.step("Get list changes history of the task.")
    def get_list_task_changes_history(self, task_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_task_changes_endpoint(task_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetListTaskChangesResultModel(result=response.json())
        logger.info(f'Successfully get list changes history of the task.')
        return model

    @allure.step("Get list of checklists in the task.")
    def get_list_task_checklists(self, task_id: int, checklist_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_task_checklists_endpoint(task_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info(f'The task with ID {task_id} does not have a checklists')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetListTaskCheckListResultModel(root=response.json())
        found = any(item.checkList.id == checklist_id for item in model.root.values())
        assert found, f'Checklist with ID {checklist_id} is not in list task checklists.'
        logger.info(f'Successfully get list of checklists in the task with ID {task_id}.')
        return model

    @allure.step("Adds checklists to the task by list.")
    def post_add_checklists_to_task_by_list(self, task_id: int, checklist_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_checklists_to_task_endpoint(task_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_checklists_to_task_payload(checklist_id)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}. {data_response}'
        model = SuccessAddChecklistsToTaskModel(result=response.json())
        logger.info(f'Successfully add checklists to the task with ID {task_id} by list.')
        return model

    @allure.step("Adds checklist to the task by id.")
    def post_add_checklists_to_task_by_id(self, task_id: int, checklist_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_checklists_to_task_by_id_endpoint(task_id, checklist_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}. {data_response}'
        model = SuccessAddChecklistsToTaskModel(result=response.json())
        logger.info(f'Successfully add checklist to the task with ID {task_id} by ID.')
        return model

    @allure.step("Delete checklists from task by list.")
    def delete_checklists_from_task_by_list(self, task_id: int, *checklist_ids: str):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_checklists_from_task_endpoint(task_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_checklists_from_task_by_list_payload(*checklist_ids)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}. {data_response}'
        logger.warning(f'Successfully delete checklists IDs {checklist_ids} from task with ID {task_id}.')

    @allure.step("Delete checklist from task by ID.")
    def delete_checklist_from_task_by_id(self, task_id: int, checklist_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_checklist_from_task_by_id_endpoint(task_id, checklist_id),
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
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}. {data_response}'
        logger.warning(f'Successfully delete checklist ID {checklist_id} from task with ID {task_id}.')

    @allure.step("Upload file to server and bind to task checklist, data from form.")
    def post_upload_attachment_to_server_bind_to_task_checklist_data_from_form(
            self,
            task_id: int,
            task_checklist_result_id: str,
            task_checklist_id: int
    ):
        file_name = f'generated_image{randint(900, 1000)}.png'
        with io.BytesIO() as image_bytes:
            with Image.new("RGB", (200, 200), color="red") as img:
                img.save(image_bytes, format="PNG")
                image_bytes.seek(0)  # Перемещаем указатель в начало

            payload = MultipartEncoder(
                fields={
                    "TaskCheckListResultID": task_checklist_result_id,
                    "Attachments.Index": "0",
                    "Attachments[0].IsIgnorePossibleDuplication": "true",
                    "Attachments[0].File": (file_name, image_bytes, 'image/png')
                }
            )
            start = time.time()
            response = requests.post(
                url=self.endpoints.post_upload_attachment_to_server_bind_to_checklist_task_from_form_endpoint(
                    task_id, task_checklist_id
                ),
                headers=self.headers.upload_file_header(get_token(), payload.content_type),
                data=payload
            )
            end = time.time()
            logger.info(response.headers)
            try:
                self.attach_response(response.json())
            except JSONDecodeError:
                logger.warning("Received response is not a valid JSON")
            self.attach_time(start, end)
            self.attach_url(response.request.url)
            assert response.status_code == HTTPStatus.CREATED, \
                f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {response.text}'
            model = SuccessUploadAttachmentsToServerTaskChecklistDataFromFormModel(**response.json())
            logger.info(f'Successfully upload file - {file_name} to server '
                        f'and bind to task {model.taskID} checklist {model.taskCheckListID}.')
            return model

    @allure.step("Get results of checklists in the task v2.")
    def get_results_task_checklists_v2(self, task_id: int, task_checklist_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_results_checklist_from_task_v2_endpoint(task_id, task_checklist_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info(f'The task with ID {task_id} does not have a checklist results')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetTaskCheckListResultV2ResultModel(root=response.json())
        logger.info(f'Successfully get results of checklist {task_checklist_id} in the task with ID {task_id}.')
        return model

    @allure.step("Get list attachments from items of checklists in the task by ID.")
    def get_list_attachments_task_checklists_items_id(
            self,
            task_id: int,
            task_checklist_id: int,
            task_checklist_result_id: int
    ):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_attachments_checklist_from_task_by_id_endpoint(
                task_id,
                task_checklist_id,
                task_checklist_result_id
            ),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info(f'The task with ID {task_id} does not have a attachments from items of checklist results')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetListAttachmentResultModel(root=response.json())
        logger.info(f'Successfully get list attachments of result task checklist '
                    f'{task_checklist_id} in the task with ID {task_id} by result ID {task_checklist_result_id}.')
        return model

    @allure.step("Get list attachments from items of checklists in the task.")
    def get_list_attachments_task_checklists_items(
            self,
            task_id: int,
            task_checklist_id: int
    ):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_attachments_checklist_from_task_endpoint(
                task_id,
                task_checklist_id
            ),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info(f'The task with ID {task_id} does not have a attachment checklist results')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetListAttachmentResultModel(root=response.json())
        logger.info(f'Successfully get list attachments of result task checklist '
                    f'{task_checklist_id} in the task with ID {task_id}.')
        return model

    @allure.step("Get data attachment from items of checklists in the task by attach ID.")
    def get_attachment_task_checklists_items_by_id(
            self,
            task_id: int,
            task_checklist_id: int,
            task_checklist_result_id: int,
            attachment_id: int
    ):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_attachment_by_id_checklist_from_task_by_id_endpoint(
                task_id,
                task_checklist_id,
                task_checklist_result_id,
                attachment_id
            ),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info(f'The task with ID {task_id} does not have a attachment checklist results')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetAttachmentByIdFromTaskChecklist(**response.json())
        logger.info(f'Successfully get list attachments of result task checklist '
                    f'{task_checklist_id} in the task with ID {task_id}.')
        return model

    @allure.step("Delete results checklist from task by list.")
    def delete_results_checklist_from_task_by_list(
            self,
            task_id: int,
            task_checklist_id: int,
            *task_results_checklist_ids: int
    ):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_results_checklist_from_task_endpoint(task_id, task_checklist_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_results_checklist_from_task_by_list_payload(*task_results_checklist_ids)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}. {data_response}'
        logger.warning(f'Successfully delete results ID {task_results_checklist_ids} '
                       f'checklist ID {task_checklist_id} from task with ID {task_id}.')

    @allure.step("Update results items of checklists in the task v2.")
    def put_update_results_task_checklists_items_v2(
            self,
            task_id: int,
            task_checklist_id: int,
            task_checklist_result_id: str,
            value,
            check: bool,
            type_item: str
    ):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_results_checklist_from_task_v2_endpoint(
                task_id,
                task_checklist_id
            ),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_results_task_checklists_items_v2_payload(
                task_checklist_result_id,
                check,
                value,
                type_item
            )
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}. {data_response}'
        model = SuccessUpdateTaskChecklistResultsModel(result=response.json())
        logger.info(f'Successfully update results items ID {model.result[0].checkListItemID} '
                    f'of checklists ID {model.result[0].taskCheckListID} in the task ID {model.result[0].taskID} v2.')
        return model

    @allure.step("Get list attachments bind to attribute task completed work by attribute ID.")
    def get_list_attachments_from_attribute_task_completed_work_by_attribute_id(
            self,
            task_id: int,
            completed_work_id: int,
            attribute_id: int
    ):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_files_attached_to_attribute_by_id_of_completed_work_by_id_on_task_endpoint(
                task_id,
                completed_work_id,
                attribute_id
            ),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info(f'The task with ID {task_id} does not have a attachments bind to attribute task completed work')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetAttributeAttachmentResultModel(root=response.json())
        logger.info(f'Successfully list attachments bind to attribute ID {attribute_id} '
                    f'task ID {task_id} completed work ID {completed_work_id}.')
        return model

    @allure.step("Get list attachments bind to attribute task completed work.")
    def get_list_attachments_from_attribute_task_completed_work(
            self,
            task_id: int,
            completed_work_id: int
    ):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_files_attached_to_attribute_of_completed_work_by_id_on_task_endpoint(
                task_id,
                completed_work_id
            ),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info(f'The task ID {task_id} does not have a attachments bind to attribute task completed work.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetAttributeAttachmentResultModel(root=response.json())
        logger.info(f'Successfully get list attachments bind to attribute'
                    f'task ID {task_id} completed work ID {completed_work_id}.')
        return model

    @allure.step("Upload file to server and bind to attribute task completed work, data from form.")
    def post_upload_attachment_to_server_bind_attribute_task_completed_work_data_from_form(
            self,
            task_id: int,
            completed_work_id: int,
            attribute_id: int
    ):
        file_name = f'generated_image{randint(1001, 1200)}.png'
        with io.BytesIO() as image_bytes:
            with Image.new("RGB", (200, 200), color="green") as img:
                img.save(image_bytes, format="PNG")
                image_bytes.seek(0)  # Перемещаем указатель в начало

            payload = MultipartEncoder(
                fields={
                    "Attachments.Index": "0",
                    "AttributeID": str(attribute_id),
                    "Attachments[0].IsIgnorePossibleDuplication": "true",
                    "Attachments[0].File": (file_name, image_bytes, 'image/png')
                }
            )
            start = time.time()
            response = requests.post(
                url=self.endpoints.post_upload_file_to_server_bind_to_completed_work_from_form_endpoint(
                    task_id, completed_work_id
                ),
                headers=self.headers.upload_file_header(get_token(), payload.content_type),
                data=payload
            )
            end = time.time()
            logger.info(response.headers)
            data_response = self.response_content(response)
            self.attach_response_headers(response.headers)
            self.attach_response(data_response)
            self.attach_time(start, end)
            self.attach_url(response.request.url)
            assert response.status_code == HTTPStatus.CREATED, \
                f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
            model = SuccessUploadAttachmentsToServerTaskCompletedWorkDataFromFormModel(**response.json())
            logger.info(f'Successfully upload file - {file_name} ID {model.attachments[0]} to server '
                        f'and bind to attribute {model.attributeID} task {model.taskID} '
                        f'completed work {model.completedWorkID}.')
            return model

    @allure.step("Get list attributes task completed work.")
    def get_list_attributes_task_completed_work(self, task_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_attributes_for_completed_work_from_task_endpoint(task_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info(f'The task with ID {task_id} does not have a attributes task completed work')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetListCompletedWorkAttributeResultModel(result=response.json())
        logger.info(f'Successfully get list attributes task ID {model.result[0].taskID} '
                    f'completed work ID {model.result[0].completedWorkID}.')
        return model

    @allure.step("Get list attributes task completed work by completed work ID.")
    def get_list_attributes_task_completed_work_by_id(self, task_id: int, completed_work_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_attributes_for_completed_work_by_id_from_task_endpoint(task_id, completed_work_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info(f'The task with ID {task_id} does not have a attributes completed work.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetListCompletedWorkAttributeResultModel(result=response.json())
        logger.info(f'Successfully get list attributes task ID {model.result[0].taskID} '
                    f'completed work ID {model.result[0].completedWorkID}.')
        return model

    @allure.step("Update attributes task completed work by completed work ID.")
    def put_update_attributes_task_completed_work_by_id(self, task_id: int, completed_work_id: int, attribute_id: int):
        value = f'Значение для доп. поля {randint(1, 99999)}'
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_attributes_for_completed_work_by_id_from_task_endpoint(
                task_id,
                completed_work_id
            ),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_attributes_task_completed_work_by_id_payload(
                attribute_id,
                value
            )
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info(f'No content')
            return None
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}. {data_response}'
        model = SuccessGetListAttributesTaskCompletedWorksModel(results=response.json())
        logger.info(f'Update attributes ID {attribute_id} task ID {task_id} '
                    f'completed work by completed work ID {completed_work_id}.')
        return model

    @allure.step("Delete attributes task completed work by list and completed work ID.")
    def delete_attributes_task_completed_work_id_by_list(
            self, task_id: int, completed_work_id: int, *attribute_ids: int
    ):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_attributes_from_completed_work_by_id_from_task_endpoint(
                task_id,
                completed_work_id
            ),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_attributes_task_completed_work_by_list_payload(*attribute_ids)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}. {data_response}'
        logger.warning(f'Success delete attributes ID {attribute_ids} task completed work by list.')

    @allure.step("Update attributes task completed work.")
    def put_update_attributes_task_completed_work(self, task_id: int, completed_work_id: int, attribute_id: int):
        value = f'Значение для доп. поля {randint(1, 99999)}'
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_attributes_completed_work_by_task_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_attributes_task_completed_work_payload(
                task_id,
                completed_work_id,
                attribute_id,
                value
            )
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info(f'No content')
            return None
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}. {data_response}'
        model = SuccessGetListAttributesTaskCompletedWorksModel(results=response.json())
        logger.info(f'Update attributes ID {attribute_id} task ID {task_id} '
                    f'completed work by completed work ID {completed_work_id}.')
        return model

    @allure.step("Delete attributes task completed work by list.")
    def delete_attributes_task_completed_work(self, task_id: int, completed_work_id: int, *attribute_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_attributes_completed_work_by_task_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_attributes_task_completed_work_payload(
                task_id,
                completed_work_id,
                *attribute_ids)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}. {data_response}'
        logger.warning(f'Success delete attributes ID {attribute_ids} task completed work by list.')

    @allure.step("Delete attribute task completed work by attribute ID.")
    def delete_attribute_task_completed_work_by_attribute_id(
            self, task_id: int, completed_work_id: int, attribute_id: int
    ):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_attribute_by_id_completed_work_by_id_from_task_endpoint(
                task_id,
                completed_work_id,
                attribute_id
            ),
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
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}. {data_response}'
        logger.warning(f'Successfully delete attribute by ID {attribute_id} task completed work.')

    @allure.step("Get list task completed work.")
    def get_list_task_completed_work(self, task_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_completed_work_from_task_endpoint(task_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info(f'The task with ID {task_id} does not have a task completed work.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetListCompletedWorkResult(result=response.json())
        logger.info(f'Successfully get list task ID {task_id} completed work.')
        return model

    @allure.step("Get task completed work by ID.")
    def get_task_completed_work_id(self, task_id: int, completed_work_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_completed_work_by_id_from_task_endpoint(task_id, completed_work_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info(f'The task with ID {task_id} does not have a task completed work.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = CompletedWorkResult(**response.json())
        logger.info(f'Successfully get task ID {task_id} completed work by ID {model.id}.')
        return model

    @allure.step("Get list attachments task completed work by complected work ID.")
    def get_list_attachments_task_completed_work_id(self, task_id: int, completed_work_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_attachments_from_completed_work_by_id_task_endpoint(task_id, completed_work_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info(f'The task with ID {task_id} does not have a attachments task completed work.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetListAttachmentsTaskCompletedWorksModel(result=response.json())
        logger.info(f'Successfully get list attachments ID {model.result[0].attachmentID} task ID {task_id} '
                    f'completed work by ID {model.result[0].completedWorkID}.')
        return model

    @allure.step("Get list attachments task completed work.")
    def get_list_attachments_task_completed_work(self, task_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_attachments_from_completed_work_task_endpoint(task_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info(f'The task with ID {task_id} does not have a attachments task completed work.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetListAttachmentsTaskCompletedWorksModel(result=response.json())
        logger.info(f'Successfully get list attachments ID {model.result[0].attachmentID} task ID {task_id} '
                    f'completed work by ID {model.result[0].completedWorkID}.')
        return model

    @allure.step("Get attachment task completed work by attachment ID.")
    def get_attachment_task_completed_work_by_attachment_id(
            self,
            task_id: int,
            completed_work_id: int,
            attachment_id: int
    ):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_temporary_redirect_attachments_completed_work_by_id_task_endpoint(
                task_id,
                completed_work_id,
                attachment_id
            ),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info(f'The task with ID {task_id} does not have a attachments task completed work.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetListAttachmentsTaskCompletedWorksModel(result=response.json())
        logger.info(f'Successfully get list attachments ID {model.result[0].attachmentID} task ID {task_id} '
                    f'completed work by ID {model.result[0].completedWorkID}.')
        return model

    @allure.step("Download attachment from task completed work by ID. No redirect")
    def get_download_attachment_from_task_completed_work_by_id_no_redirect(
            self,
            task_id: int,
            completed_work_id: int,
            attachment_id: int
    ):
        param = {
            "noRedirect": True
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_temporary_redirect_attachments_completed_work_by_id_task_endpoint(
                task_id,
                completed_work_id,
                attachment_id
            ),
            params=param,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected {HTTPStatus.OK}, but got {response.status_code}. Message {data_response}'
        model = SuccessGetAttachmentLinkNoRedirectModel(**response.json())
        logger.info(f'Successfully get download attachment {attachment_id} from task {task_id} completed work by id.')
        return model

    @allure.step("Download attachment from task completed work by ID.")
    def get_download_attachment_from_task_completed_work_by_id(
            self,
            task_id: int,
            completed_work_id: int,
            attachment_id: int
    ):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_temporary_redirect_attachments_completed_work_by_id_task_endpoint(
                task_id,
                completed_work_id,
                attachment_id
            ),
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
        assert response.status_code == HTTPStatus.OK, \
            f'Expected {HTTPStatus.OK}, but got {response.status_code}. Message {response.text}'
        assert response.content, "Response content is empty, expected file data"
        assert response.headers.get("Content-Type") is not None, "Content-Type header is missing"
        assert "application/octet-stream" in response.headers["Content-Type"] or "application/" in response.headers[
            "Content-Type"], \
            f"Unexpected Content-Type: {response.headers['Content-Type']}"
        logger.info(f'Successfully get download attachment {attachment_id} '
                    f'from task ID {task_id} completed work {completed_work_id} by ID.')

    @allure.step("Add materials to task completed work.")
    def post_add_materials_task_completed_work(
            self,
            task_id: int,
            completed_work_id: int,
            material_id: int,
            warehouse_id: int,
            inventory_id: int,
            measurement_unit_id: int,
            user_id: int
    ):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_materials_from_completed_work_task_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_materials_to_task_completed_work_payload(
                task_id,
                completed_work_id,
                material_id,
                warehouse_id,
                inventory_id,
                measurement_unit_id,
                1,
                user_id,
                10,
                1
            )
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}. {data_response}'
        model = SuccessAddMaterialsTaskComplectedWork(results=response.json())
        logger.info(f'Successfully add materials ID {model.results[0].materialID} to '
                    f'task ID {model.results[0].taskID} completed work ID {model.results[0].completedWorkID}')
        return model

    @allure.step("Add technicians to task completed work.")
    def post_add_technicians_task_completed_work(
            self,
            task_id: int,
            completed_work_id: int,
            user_id: int
    ):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_technicians_to_completed_works_task_endpoints,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_technicians_to_task_completed_work_payload(
                task_id,
                completed_work_id,
                10,
                user_id,
                1,
            )
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}. {data_response}'
        model = SuccessAddTechniciansTaskComplectedWorkModel(results=response.json())
        logger.info(f'Successfully add technicians ID {model.results[0].userID} to '
                    f'task ID {model.results[0].taskID} completed work ID {model.results[0].completedWorkID}')
        return model

    @allure.step("Get list materials task completed work.")
    def get_list_materials_task_completed_work(self, task_id: int, completed_work_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_materials_from_completed_work_by_id_task_endpoint(task_id, completed_work_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info(f'The task with ID {task_id} does not have a attachments task completed work.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetListCompletedWorkMaterialResultModel(**response.json())
        logger.info(f'Successfully get list materials ID {model.materials[0].materialID} task ID {task_id} '
                    f'completed work by ID {model.completedWorkID}.')
        return model

    @allure.step("Delete materials task completed work by completed work ID.")
    def delete_materials_task_completed_work(
            self,
            task_id: int,
            completed_work_id: int,
            material_id: int,
            wh_id: int,
            inventory_id: int
    ):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_materials_from_completed_work_by_id_task_endpoint(task_id, completed_work_id),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_materials_task_completed_work_payload(
                material_id,
                wh_id,
                inventory_id
            )
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}. {data_response}'
        logger.warning(f'Successfully delete materials {material_id} '
                       f'from task {task_id} completed work {completed_work_id}.')

    @allure.step("Get list materials all task completed work.")
    def get_list_materials_all_task_completed_work(self, task_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_materials_from_completed_work_task_endpoint(task_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info(f'The task with ID {task_id} does not have a attachments task completed work.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetListRootCompletedWorkMaterialResultModel(root=response.json())
        logger.info(f'Successfully get list materials all task ID {task_id} completed work.')
        return model

    @allure.step("Update materials to task completed work.")
    def put_update_materials_task_completed_work(
            self,
            task_id: int,
            completed_work_id: int,
            material_id: int,
            warehouse_id: int,
            inventory_id: int,
            measurement_unit_id: int,
            user_id: int
    ):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_materials_from_completed_work_task_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_materials_to_task_completed_work_payload(
                task_id,
                completed_work_id,
                material_id,
                warehouse_id,
                inventory_id,
                measurement_unit_id,
                2,
                user_id,
                20,
            )
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}. {data_response}'
        logger.info(f'Successfully update materials ID {material_id} task ID {task_id}'
                    f'completed work ID {completed_work_id}.')

    @allure.step("Delete materials task completed works.")
    def delete_materials_task_completed_works(
            self,
            task_id: int,
            completed_work_id: int,
            material_id: int,
            wh_id: int,
            inventory_id: int
    ):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_materials_from_completed_work_task_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_materials_from_task_completed_works_payload(
                task_id,
                completed_work_id,
                material_id,
                wh_id,
                inventory_id
            )
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}. {data_response}'
        logger.warning(f'Successfully delete materials {material_id} '
                       f'from task {task_id} completed work {completed_work_id}.')

    @allure.step("Upload file to server and bind to report task completed work, data from form.")
    def post_upload_attachment_to_server_bind_report_task_completed_work_data_from_form(
            self,
            task_id: int
    ):
        file_name = f'generated_image{randint(1001, 1200)}.jpeg'
        with io.BytesIO() as image_bytes:
            with Image.new("RGB", (500, 500), color="green") as img:
                img.save(image_bytes, format="JPEG")
                image_bytes.seek(0)  # Перемещаем указатель в начало

            payload = MultipartEncoder(
                fields={
                    "TaskID": str(task_id),
                    "AIsIgnorePossibleDuplication": "true",
                    "File": (file_name, image_bytes, 'image/jpeg')
                }
            )
            start = time.time()
            response = requests.post(
                url=self.endpoints.post_upload_attachment_bind_to_report_completed_work_task_from_form_endpoint,
                headers=self.headers.upload_file_header(get_token(), payload.content_type),
                data=payload
            )
            end = time.time()
            logger.info(response.headers)
            data_response = self.response_content(response)
            self.attach_response_headers(response.headers)
            self.attach_response(data_response)
            self.attach_time(start, end)
            self.attach_url(response.request.url)
            assert response.status_code == HTTPStatus.CREATED, \
                f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
            model = SuccessUploadAttachToReportTaskCompletedWorkModel(**response.json())
            logger.info(f'Successfully upload file {model.attachmentID} '
                        f'to server and bind to report task ID {task_id} completed work.')
            return model

    @allure.step("Get signature from report task completed work.")
    def get_signature_report_task_completed_work(self, task_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_report_attachment_from_completed_work_task_endpoint(task_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info(f'The task with ID {task_id} does not have a attachments report task completed work.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SignatureReportAttachmentModel(**response.json())
        logger.info(f'Successfully get signature report task ID {model.taskID} completed work.')
        return model

    @allure.step("Delete signature report task completed works.")
    def delete_signature_report_task_completed_works(
            self,
            task_id: int,
            attachment_id: int,
    ):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_attachment_by_id_report_completed_work_task_endpoint(
                task_id, attachment_id
            ),
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}. {data_response}'
        logger.warning(f'Successfully delete signature (attachment {attachment_id} report'
                       f'from task {task_id} completed work.')

    @allure.step("Add uploaded signature to report task completed works.")
    def post_add_uploaded_signature_to_report_task_completed_works(
            self,
            task_id: int,
            attachment_id: int
    ):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_attachment_by_id_report_completed_work_task_endpoint(
                task_id, attachment_id
            ),
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}. {data_response}'
        logger.info(f'Successfully bind uploaded signature ID {attachment_id} '
                    f'and report task ID {task_id} completed works.')

    @allure.step("Add uploaded signature to report task completed works V2.")
    def post_add_uploaded_signature_to_report_task_completed_works_v2(
            self,
            task_id: int,
            attachment_id: int
    ):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_attachment_by_id_report_completed_work_task_v2_endpoint(
                task_id, attachment_id
            ),
            headers=self.headers.basic_header(get_token()),
            # json=self.payloads.post_add_uploaded_signature_to_report_task_completed_works_v2_payload(
            #     'Обслуживание',
            #     'Работник'
            # )
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        # self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}. {data_response}'
        logger.info(f'Successfully bind uploaded signature ID {attachment_id} '
                    f'and report task ID {task_id} completed works V2.')

    @allure.step("Uploads the file to server and binds it to report task completed works, data from body.")
    def post_upload_signature_to_report_task_completed_works_data_from_body(self, task_id: int):
        file_name = f'signature_from_body{randint(1, 999)}.png'
        with (io.BytesIO() as image_bytes):
            # Генерация изображения (например, 150x150 пикселей, синий фон)
            with Image.new("RGB", (150, 150), color="blue") as img:
                img.save(image_bytes, format="PNG")
                image_bytes.seek(0)  # Перемещаем указатель в начало
                # Преобразование изображения в строку Base64
                image_base64 = base64.b64encode(image_bytes.read()).decode('utf-8')

            payload = {
                "taskID": task_id,
                "FileName": file_name,
                "ContentType": "image/png",
                "Description": "Файл из тела запроса загружен авто тестом",
                "isPublic": False,
                "IsIgnorePossibleDuplication": True,
                "File": image_base64
            }
            start = time.time()
            response = requests.post(
                url=self.endpoints.post_upload_attachment_bind_to_report_completed_work_task_from_body_endpoint,
                headers=self.headers.basic_header(get_token()),
                json=payload
            )
            end = time.time()
            logger.info(response.headers)
            data_response = self.response_content(response)
            self.attach_response(data_response)
            self.attach_response_headers(response.headers)
            self.attach_time(start, end)
            self.attach_url(response.request.url)
            self.attach_request(response.request.body)
            assert response.status_code == HTTPStatus.CREATED, \
                f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
            model = SuccessUploadAttachToReportTaskCompletedWorkModel(**response.json())
            logger.info(f'Successfully upload {file_name} to task ID {task_id} completed works, data from body.')
            return model

    @allure.step("Get list technicians from task completed work.")
    def get_list_technicians_task_completed_work(self, task_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_technicians_from_completed_work_task_endpoint(task_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info(f'The task with ID {task_id} does not have a technicians task completed work.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetListCompletedWorkTechnicianResult(root=response.json())
        logger.info(f'Successfully get list technicians task ID {task_id} completed work.')
        return model

    @allure.step("Get list technicians from task completed work by completed work ID.")
    def get_list_technicians_task_completed_work_completed_work_id(self, task_id: int, completed_work_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_technicians_from_completed_work_by_id_task_endpoint(
                task_id, completed_work_id
            ),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info(f'The task with ID {task_id} does not have a technicians task completed work.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = CompletedWorkTechnicianResult(**response.json())
        logger.info(f'Successfully get list technicians task ID {task_id} completed work by ID {completed_work_id}.')
        return model

    @allure.step("Delete technicians task completed works by list.")
    def delete_technicians_task_completed_works_by_list(
            self,
            task_id: int,
            completed_work_id: int,
            *technicians_ids: int
    ):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_technicians_from_completed_work_task_endpoint(
                task_id, completed_work_id
            ),
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_technicians_task_completed_works_by_list_payload(
                *technicians_ids
            )
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}. {data_response}'
        logger.warning(f'Successfully delete technicians {technicians_ids}'
                       f'from task {task_id} completed work.')

    @allure.step("Update technician task completed work.")
    def put_update_technician_task_completed_work(
            self,
            task_id: int,
            completed_work_id: int,
            user_id: int
    ):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_technicians_from_completed_works_task_endpoints,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_technician_task_completed_work_payload(
                task_id,
                completed_work_id,
                20,
                user_id,
                2,
            )
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}. {data_response}'
        logger.info(f'Successfully update technicians ID {user_id} to '
                    f'task ID {task_id} completed work ID {completed_work_id}')

    @allure.step("Delete technicians from task completed work.")
    def delete_technicians_from_task_completed_work(
            self,
            task_id: int,
            completed_work_id: int,
            *user_ids: int
    ):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_technicians_from_completed_works_task_endpoints,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_technician_from_task_completed_work_payload(
                task_id,
                completed_work_id,
                *user_ids,
                )
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}. {data_response}'
        logger.info(f'Successfully delete technicians ID {user_ids} from '
                    f'task ID {task_id} completed work ID {completed_work_id}')

    @allure.step("Get list contacts from task.")
    def get_list_contacts_from_task(self, task_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_contacts_from_task_endpoint(task_id),
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info(f'The task with ID {task_id} does not have a contacts task completed work.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetTaskContactsListResultModel(root=response.json())
        logger.info(f'Successfully get list contacts from task ID {task_id}.')
        return model

    @allure.step("Get contact from task by id.")
    def get_contact_from_task_by_id(self, task_id: int, contact_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_contact_by_id_from_task_endpoint(task_id, contact_id),
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = TaskContactsListResultModel(**response.json())
        logger.info(f'Successfully get contact ID {contact_id} from task ID {task_id}.')
        return model

    @allure.step("Delete contact from task by contact id.")
    def delete_contact_from_task_by_contact_id(self, task_id: int, contact_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_contact_by_id_from_task_endpoint(task_id, contact_id),
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}. {data_response}'
        logger.warning(f'Successfully delete contact ID {contact_id} from task ID {task_id}.')

    @allure.step("Get list conversations from task.")
    def get_conversations_from_task(self, task_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_conversations_from_task_endpoint(task_id),
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info(f'The task with ID {task_id} does not have a conversations.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetListTaskMessageModel(results=response.json())
        logger.info(f'Successfully get list conversations from task ID {task_id}.')
        return model

    @allure.step("Head conversations from task.")
    def head_conversations_from_task(self, task_id: int):
        start = time.time()
        response = requests.head(
            url=self.endpoints.head_conversations_from_task_endpoint(task_id),
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        items_conversations = response.headers.get("Content-Range", "")
        if "/" in items_conversations:
            qty_conversations = int(items_conversations.split("/")[1])
            logger.info(f'Successfully get head qty: {qty_conversations} conversations from task ID {task_id}.')
            return qty_conversations
        else:
            logger.info("Content-Range header does not contain the number of conversations")

    @allure.step("Get conversation from task by id.")
    def get_conversation_from_task_by_id(self, task_id: int, conversation_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_conversation_by_id_from_task_endpoint(task_id, conversation_id),
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info(f'The task with ID {task_id} does not have a conversations.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = TaskMessageModel(**response.json())
        logger.info(f'Successfully get conversation by id {conversation_id} from task ID {task_id}.')
        return model

    @allure.step("Upload file to server and bind to conversation task, data from form.")
    def post_upload_attachment_to_server_bind_conversation_task_data_from_form(
            self,
            task_id: int
    ):
        file_name = f'generated_image{randint(2000, 2999)}.png'
        with io.BytesIO() as image_bytes:
            with Image.new("RGB", (200, 200), color="red") as img:
                img.save(image_bytes, format="PNG")
                image_bytes.seek(0)  # Перемещаем указатель в начало

            payload = MultipartEncoder(
                fields={
                    "IsExternal": "false",
                    "Attachments.Index": "0",
                    "Attachments[0].AIsIgnorePossibleDuplication": "true",
                    "Attachments[0].File": (file_name, image_bytes, 'image/png')
                }
            )
            start = time.time()
            response = requests.post(
                url=self.endpoints.post_upload_attachments_to_conversation_task_from_form_endpoint(task_id),
                headers=self.headers.upload_file_header(get_token(), payload.content_type),
                data=payload
            )
            end = time.time()
            logger.info(response.headers)
            data_response = self.response_content(response)
            self.attach_response_headers(response.headers)
            self.attach_response(data_response)
            self.attach_time(start, end)
            self.attach_url(response.request.url)
            assert response.status_code == HTTPStatus.CREATED, \
                f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
            model = SuccessUploadAttachmentsToServerTaskConversationDataFromFormModel(**response.json())
            logger.info(f'Successfully upload file {model.attachments[0]} '
                        f'to server and bind to conversation task ID {task_id}.')
            return model

    @allure.step("Download attachment from conversation task by ID.")
    def get_download_attachment_from_conversation_task_by_id(
            self,
            task_id: int,
            conversation_id: int,
            attachment_id: int
    ):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_temporary_redirect_attachment_conversations_task_endpoint(
                task_id,
                conversation_id,
                attachment_id
            ),
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
        assert response.status_code == HTTPStatus.OK, \
            f'Expected {HTTPStatus.OK}, but got {response.status_code}. Message {response.text}'
        assert response.content, "Response content is empty, expected file data"
        assert response.headers.get("Content-Type") is not None, "Content-Type header is missing"
        assert "application/octet-stream" in response.headers["Content-Type"] or "application/" in response.headers[
            "Content-Type"], \
            f"Unexpected Content-Type: {response.headers['Content-Type']}"
        logger.info(f'Successfully get download attachment {attachment_id} '
                    f'from task ID {task_id} conversation {conversation_id} by ID.')

    @allure.step("Get info conversation delivery from task by id.")
    def get_info_conversation_delivery_from_task_by_id(self, task_id: int, conversation_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_conversation_delivery_status_task_endpoint(task_id, conversation_id),
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info(f'The task with ID {task_id} does not have a conversations.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetListConversationDeliveryResult(results=response.json())
        logger.info(f'Successfully get info conversation delivery by id {conversation_id} from task ID {task_id}.')
        return model

    @allure.step("Update (PATCH) Notes field in the task by id.")
    def patch_update_field_notes_in_task_by_id(self, task_id: int):
        note = f"Заметка-{randint(1, 999)}"
        field = [
            {
                "field": "Notes",
                "value": note
            }
        ]
        start = time.time()
        response = requests.patch(
            url=self.endpoints.patch_task_by_id_endpoint(task_id),
            headers=self.headers.basic_header(get_token()),
            json=field
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}. {data_response}'
        logger.info(f'Successfully update (PATCH) Notes field in the task ID {task_id}.')
        return note

    @allure.step("Update (PATCH) number field in the task by id.")
    def patch_update_field_number_in_task_by_id(
            self,
            task_id: int,
            task_number: int or str,
            status_code: int,
            len_task_number: int
    ) -> None:
        field = [
            {
                "field": "number",
                "value": task_number
            }
        ]
        start = time.time()
        response = requests.patch(
            url=self.endpoints.patch_task_by_id_endpoint(task_id),
            headers=self.headers.basic_header(get_token()),
            json=field
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == status_code, \
            f'Expected status code {status_code}, but got {response.status_code}, {data_response}'
        match response.status_code:
            case HTTPStatus.BAD_REQUEST:
                model = ErrorModel(list_model=response.json())
                logger.warning(f'{response.status_code}: {model.list_model[0].message}')
                return None
            case HTTPStatus.CONFLICT:
                model = ErrorModel(list_model=response.json())
                logger.warning(f'{response.status_code}: {model.list_model[0].message}')
                return None
        model_get_task = self.get_detailed_info_task_by_id(task_id)
        assert len(model_get_task.number) == len_task_number, \
            f'Expected {len_task_number}, but got {len(model_get_task.number)}'
        logger.info(f'Successfully update (PATCH) number field in the task ID {task_id}.')

    @allure.step("Delete task by list.")
    def delete_task_by_list(self, *task_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_task_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_task_by_list_payload(*task_ids)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}. {data_response}'
        model = SuccessDeleteTaskModel(list=response.json())
        logger.warning(f'Successfully delete task IDs {task_ids}.')
        return model

    @allure.step("Delete mass tasks by list.")
    def delete_mass_tasks_by_list(self, list_tasks_ids: List[int]):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_task_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=list_tasks_ids
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}. {data_response}'
        model = SuccessDeleteTaskModel(list=response.json())
        logger.warning(f'Successfully delete mass tasks qty IDs {len(list_tasks_ids)}.')
        return model

    @allure.step("Get info the company code is used when generating the task number.")
    def get_info_check_company_code_used(self, task_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_check_company_code_used_task_by_id_endpoint(task_id),
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetUsedCompanyCodeInTaskNumberModel(result=response.json())
        logger.info(f'Successfully get info the company code is used when generating the task ({task_id}) number.')
        return model

    @allure.step("Head task by ID.")
    def head_task_by_id(self, task_id: int):
        params = {
            "taskID": task_id
        }
        start = time.time()
        response = requests.head(
            url=self.endpoints.head_task_endpoint, params=params,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        items_head = response.headers.get("Content-Range", "")
        if "/" in items_head:
            qty_tasks = int(items_head.split("/")[1])
            logger.info(f'Successfully get head qty: {qty_tasks} task ID {task_id}.')
            return qty_tasks
        else:
            logger.info("Content-Range header does not contain the number of task")

    @allure.step("Head task.")
    def head_task(self):
        start = time.time()
        response = requests.head(
            url=self.endpoints.head_task_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        logger.info(f'Successfully get head task.')

    @allure.step("Get short list tasks.")
    def get_short_list_tasks(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_short_list_task_endpoint,
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info('NO CONTENT: status code 204.')
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessListShortResultModel(root=response.json())
        logger.info(f'Successfully get short list tasks.')
        return model

    @allure.step("Marks the task as completed.")
    def put_task_completed(self, task_id: int, token):
        self.sleep_with_progress_bar(15)
        now = datetime.now(timezone.utc)
        date_now = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        closed_date = date_now
        completed_date = date_now
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_mark_task_as_completed_endpoint(task_id),
            headers=self.headers.basic_header(token),
            json=self.payloads.put_task_completed_payload(closed_date, completed_date)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}. {data_response}'
        logger.info(f'Successfully marks the task ID {task_id} as completed.')

    @allure.step("Restore deleted task by list.")
    def put_restore_deleted_tasks_by_list(self, *task_ids: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_restore_task_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_restore_deleted_task_by_list_payload(*task_ids)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}. {data_response}'
        logger.info(f'Successfully restore deleted task ID {task_ids} by list.')

    @allure.step("Get count list tasks by day (yesterday, now).")
    def get_count_list_tasks_by_day(self):
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        date_now = now.strftime("%Y-%m-%d")
        date_yesterday = yesterday.strftime("%Y-%m-%d")
        date_params = {
            "dateFrom": date_yesterday,
            "dateTill": date_now
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_count_task_by_day_endpoint, params=date_params,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info('NO CONTENT: status code 204.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetListCountResultModel(root=response.json())
        logger.info(f'Successfully get count list tasks by day (yesterday, now).')
        return model

    @allure.step("Get short list of tasks clustered by geo-area hash code (clustering).")
    def get_short_list_tasks_by_geo_area_hash_code(self):
        geo_params = {
            "pointNorthEast": "60.926911:31.344491",
            "pointSouthWest": "59.926911:30.344491"
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_short_list_of_task_clustered_by_geo_hash_endpoint, params=geo_params,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info('NO CONTENT: status code 204.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetTaskGroupByResultModel(results=response.json())
        logger.info(f'Successfully get short list of tasks clustered by geo-area hash code (clustering).')
        return model

    @allure.step("Get list materials of task.")
    def get_list_materials_task(self, task_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_materials_for_task_endpoint(task_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info('NO CONTENT: status code 204.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessTaskMaterialsModel(root=response.json())
        logger.info(f'Successfully get list materials of task.')
        return model

    @allure.step("Get metadata for the task form.")
    def get_metadata_for_task_form(self, task_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_meta_data_for_form_task_endpoint(task_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info('NO CONTENT: status code 204.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = TaskFormMetadataResultModel(**response.json())
        logger.info(f'Successfully get metadata for the task form.')
        return model

    @allure.step("Get metadata for the tasks form (new).")
    def get_metadata_for_tasks_form_new(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_meta_new_data_for_form_task_endpoint,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info('NO CONTENT: status code 204.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetTaskFormMetadataResultModel(root=response.json())
        logger.info(f'Successfully get metadata for the task form (new).')
        return model

    @allure.step("Get technician reviews/ratings on the task.")
    def get_technician_ratings_avg_on_task(self, task_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_ratings_avg_engineers_task_endpoint(task_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info('NO CONTENT: status code 204.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetListRatingResultModel(results=response.json())
        logger.info(f'Successfully technician reviews/ratings on the task.')
        return model

    @allure.step("Get technician ratings on the task.")
    def get_technician_ratings_on_task(self, task_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_ratings_engineers_task_endpoint(task_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info('NO CONTENT: status code 204.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetListRatingResultModel(results=response.json())
        logger.info(f'Successfully technician ratings on the task.')
        return model

    @allure.step("Get skills from task.")
    def get_skills_from_task(self, task_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_skills_task_endpoint(task_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.info('NO CONTENT: status code 204.')
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetTaskSkillResultModel(root=response.json())
        logger.info(f'Successfully skills from task.')
        return model

    @allure.step("Activates the scheduled automatic transition through the task stages.")
    def post_activate_task_auto_staging(self, task_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_activate_auto_staginging_task_endpoint(task_id),
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
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}. {data_response}'
        logger.info(f'Successfully activates the scheduled automatic transition through the task stages.')

    @allure.step("Deactivate the scheduled automatic transition through the task stages.")
    def delete_deactivate_task_auto_staging(self, task_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_deactivate_auto_staginging_task_endpoint(task_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        logger.info(f'Successfully deactivates the scheduled automatic transition through the task stages.')

    @allure.step("Get the history of the tasks movement through the stages.")
    def get_task_stages(self, task_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_history_stages_task_endpoint(task_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetListStagingHistoryResultModel(results=response.json())
        logger.info(f'Successfully get the history of the tasks movement through the stages.')
        return model

    @allure.step("Get list of available stages to which tasks from the list can be transferred.")
    def get_task_stages_next(self, *task_ids: int):
        param = [('id', task_id) for task_id in task_ids]
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_available_next_stages_to_task_from_list_endpoint, params=param,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetListStagesNextModel(results=response.json())
        logger.info(f'Successfully get list of available stages to which tasks from the list can be transferred.')
        return model

    @allure.step("Get list of available stages to which tasks from the list can be transferred by list tasks.")
    def get_task_stages_next_by_list(self, list_tasks: List[int]):
        param = [('id', task_id) for task_id in list_tasks]
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_available_next_stages_to_task_from_list_endpoint, params=param,
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetListStagesNextModel(results=response.json())
        logger.info(f'Successfully get list of available stages to which tasks from the list can be transferred.')
        return model

    @allure.step("Get task tags.")
    def get_task_tags(self, task_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_tags_task_endpoint(task_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetListTaskTagsModel(results=response.json())
        logger.info(f'Successfully get task tags <{model.results[0]}>.')
        return model

    @allure.step("Get task watch lists.")
    def get_task_watch_lists(self, task_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_watch_list_by_task_endpoint(task_id),
            headers=self.headers.basic_header(get_token())
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}. {data_response}'
        model = SuccessGetListTaskWatchListsListResultModel(results=response.json())
        logger.info(f'Successfully get task watch lists.')
        return model
