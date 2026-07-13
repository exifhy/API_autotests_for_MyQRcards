import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.common.common_power_bi_reports.payloads import Payloads
from services.common.common_power_bi_reports.endpoints import Endpoints
from config.headers import Headers
from services.common.common_power_bi_reports.models.common_power_bi_reports_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class CommonPowerBIReportsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get list power BI reports.")
    def get_list_power_bi_reports(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_power_bi_reports_endpoint,
            headers=self.headers.basic_header(get_token()),
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list of power BI reports.")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}, {data_response}')
        model = SuccessGetPowerBIReportResultModel(results=response.json())
        logger.info(f'Successfully get list power BI reports.')
        return model

    @allure.step("Get power BI report by ID.")
    def get_power_bi_report_by_id(self, report_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_power_bi_report_by_id_endpoint(report_id),
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
            (f'Expected status code {HTTPStatus.OK}, '
             f'but got {response.status_code}, {data_response}')
        model = PowerBIReportResultModel(**response.json())
        logger.info(f'Successfully get power BI report by ID {report_id}.')
        return model
