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
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = LayoutTemplateDtoModel(root=response.json())
        logger.info(f'Successfully get task layout templates.')
        return model
