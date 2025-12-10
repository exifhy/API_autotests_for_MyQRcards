import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.wh.wh_document_types.payloads import Payloads
from services.wh.wh_document_types.endpoints import Endpoints
from config.headers import Headers
from services.wh.wh_document_types.models.wh_document_types_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class WhDocumentTypesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get document types.")
    def get_document_types(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_document_types_endpoint,
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
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessGetListDocumentTypesResult(root=response.json())
        logger.info(f'Successfully get list document types.')
        return model
