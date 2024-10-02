import os
import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.adm.adm_tenant_members.payloads import Payloads
from services.adm.adm_tenant_members.endpoints import Endpoints
from config.headers import Headers
from services.adm.adm_tenant_members.models.adm_tenant_members_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv


load_dotenv()
APP_ID = os.getenv('APP_ID')
API_TOKEN = os.getenv('API_TOKEN')


class AdmTenantMembersAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Marks the tenant member as deleted.")
    def delete_tenant_member_by_id(self, tenant_member_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_tenant_member_by_id_endpoint(tenant_member_id),
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.error("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.CREATED, response.status_code
        logger.info(f'Successfully marks the tenant member as deleted.')
