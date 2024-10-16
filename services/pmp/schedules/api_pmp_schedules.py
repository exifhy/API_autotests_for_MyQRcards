from datetime import datetime, timedelta
import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.pmp.schedules.payloads import Payloads
from services.pmp.schedules.endpoints import Endpoints
from config.headers import Headers
from services.pmp.schedules.models.pmp_schedules_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class PmpSchedulesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add schedule for tenant.")
    def post_add_schedule(self):
        date = datetime.today() + timedelta(1)
        tomorrow = date.strftime('%Y-%m-%d')
        start = time.time()
        response = requests.post(
            url=self.endpoints.add_update_schedules_for_tenant_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.add_during_day_schedule_for_tenant_payload(
                date_from=f"{tomorrow}T00:00:00",
                date_till=f"{tomorrow}T23:59:59"
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
        assert response.status_code == HTTPStatus.OK, f'{response.status_code}, {response.json()}'
        model = SuccessAddSchedulesModel(schedules=response.json())
        logger.info(f'Successfully created schedules. {model.schedules[0]}')
        return model

    @allure.step("Deleting a schedule for a tenant by id.")
    def delete_schedule_by_id(self, schedule_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_schedules_endpoint(schedule_id),
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
        assert response.status_code == HTTPStatus.ACCEPTED, f'{response.status_code}, {response.json()}'
        logger.info(f'Successfully deleting a schedule for a tenant by id.')

