import random
import allure
import requests
from datetime import timezone
from loguru import logger
from requests import JSONDecodeError
from requests_toolbelt import MultipartEncoder
from PIL import Image
import io
from utils.helper import Helper
from services.work.tasks.payloads import Payloads
from services.work.tasks.endpoints import Endpoints
from config.headers import Headers
from services.work.tasks.models.work_tasks_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from random import randint


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


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
        task_number = str(random.randint(999, 99999))
        note_task = f'Заявка создана авто-тестом'
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_task_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
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
        logger.info(f'Successfully add a task, number task: {task_number}')
        return model

    @allure.step("Delete the task.")
    def delete_task_by_id(self, task_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_task_by_id_endpoint(task_id),
            headers=self.headers.basic_header(API_TOKEN),
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
            headers=self.headers.basic_header(API_TOKEN),
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

    @allure.step("Returns detailed information on the task by id.")
    def get_detailed_info_task_by_id(self, task_id: int):
        # params = {
        #     "taskSnapshotID": int,
        #     "includeSchedule": bool
        # }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_detailed_info_task_by_id_endpoint(task_id),
            headers=self.headers.basic_header(API_TOKEN),
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
        model = SuccessDetailedInfoModel(**response.json())
        logger.info(f'Successfully returns detailed information on the task by id.')
        return model

    @allure.step("Update task by id.")
    def put_update_task_by_id(self, task_id: int):
        date = datetime.now(timezone.utc).isoformat(timespec='milliseconds')
        current_time_iso = date.replace('+00:00', 'Z')
        task_number = str(random.randint(999, 99999))
        note_task = 'Заявка изменена авто-тестом'
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_task_by_id_endpoint(task_id),
            headers=self.headers.basic_header(API_TOKEN),
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
            headers=self.headers.basic_header(API_TOKEN),
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
            token = API_TOKEN
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
            headers=self.headers.basic_header(API_TOKEN),
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
            headers=self.headers.basic_header(API_TOKEN),
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
            headers=self.headers.basic_header(API_TOKEN),
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
                f'Expected {model_attachment.fileName}, but got {model.root[str(model_attachment.attachmentID)].fileName}'
            logger.info(f'Successfully get the list task ID {task_id} attachment ID {model_attachment.attachmentID}.')
            return model

    @allure.step("Get task attachment by ID.")
    def get_task_attachment_by_id(self, task_id: int, model_attachment):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_task_attachment_by_id_endpoint(task_id, model_attachment.attachmentID),
            headers=self.headers.basic_header(API_TOKEN),
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
            headers=self.headers.basic_header(API_TOKEN)
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
            headers=self.headers.basic_header(API_TOKEN)
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
            headers=self.headers.basic_header(API_TOKEN)
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
            headers=self.headers.basic_header(API_TOKEN)
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
            headers=self.headers.basic_header(API_TOKEN)
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
            headers=self.headers.basic_header(API_TOKEN)
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
        assert checklist_id == model.root['1'].checkList.id, \
            f'Checklist with ID {checklist_id} is not in list task checklists.'
        logger.info(f'Successfully get list of checklists in the task with ID {task_id}.')
        return model

    @allure.step("Adds checklists to the task by list.")
    def post_add_checklists_to_task_by_list(self, task_id: int, checklist_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_checklists_to_task_endpoint(task_id),
            headers=self.headers.basic_header(API_TOKEN),
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
            headers=self.headers.basic_header(API_TOKEN)
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
            headers=self.headers.basic_header(API_TOKEN),
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
            headers=self.headers.basic_header(API_TOKEN)
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
                headers=self.headers.upload_file_header(API_TOKEN, payload.content_type),
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
            headers=self.headers.basic_header(API_TOKEN)
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
