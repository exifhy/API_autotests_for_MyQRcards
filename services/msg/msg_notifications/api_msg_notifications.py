import allure
import requests
from loguru import logger
from utils.helper import Helper
from utils.token_utils import get_token
from services.msg.msg_notifications.payloads import Payloads
from services.msg.msg_notifications.endpoints import Endpoints
from config.headers import Headers
from services.msg.msg_notifications.models.msg_notifications_model import *
import time
from http import HTTPStatus


class MSGNotificationsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get list of unread notifications.")
    def get_list_of_unread_notifications(self):
        param = {
            "includeIsViewed": False
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_notifications_endpoint, params=param,
            headers=self.headers.basic_header_with_range(get_token())
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
             f'but got {response.status_code}. {data_response}.')
        model = NotificationListResultModel(root=response.json())
        logger.info(f'Successfully get list of unread notifications.')
        return model

    @allure.step("Get list of unread notifications about mass movement of tasks by stages.")
    def get_list_of_unread_notifications_about_mass_movement_tasks_by_stages(self, tasks: int, seconds: int):
        self.sleep_with_progress_bar(seconds)
        param = {
            "includeIsViewed": True
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_notifications_endpoint, params=param,
            headers=self.headers.basic_header_with_range(get_token())
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
             f'but got {response.status_code}. {data_response}.')
        model = NotificationListResultModel(root=response.json())
        assert "Массовый перевод заявок по стадиям успешно завершён" == model.root[next(iter(model.root))].subject, \
            (f"Expected <Массовый перевод заявок по стадиям успешно завершён>, "
             f"but got {model.root[next(iter(model.root))].subject}")
        assert str(tasks) in model.root[next(iter(model.root))].content, \
            f"Expected {tasks} in {model.root[next(iter(model.root))].content}"
        logger.info(f'Successfully get list of unread notifications about mass movement of tasks by stages.')
        return model
