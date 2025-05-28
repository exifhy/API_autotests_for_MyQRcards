import os
import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.adm.adm_tenant_members.payloads import Payloads
from services.adm.adm_tenant_members.endpoints import Endpoints
from config.headers import Headers
from services.adm.adm_tenant_members.models.adm_tenant_members_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token
from dotenv import load_dotenv


load_dotenv()
APP_ID = os.getenv('APP_ID')


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
            headers=self.headers.basic_header(get_token())
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
        logger.warning(f'Successfully marks the tenant member as deleted.')

    @allure.step("Returns the API user in the current tenant.")
    def get_returns_api_user_in_current_tenant(self, access_token: str):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_returns_api_user_in_current_tenant_endpoint,
            headers=self.headers.authorization_header(access_token, APP_ID)
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list of API user.")
            return None
        assert response.status_code == HTTPStatus.OK, f'{response.status_code}, {response.json()}'
        model = SuccessTenantMembersListResultModel(**response.json())
        logger.info(f'Successfully returns the API user in the current tenant.')
        return model

    @allure.step("Get API user in the current tenant.")
    def get_api_user_in_current_tenant(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_returns_api_user_in_current_tenant_endpoint,
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
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list of API user.")
            return None
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code {HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessTenantMembersListResultModel(**response.json())
        logger.info(f'Successfully get API user in the current tenant.')
        return model

    @allure.step("Get tenant member by ID.")
    def get_tenant_member_by_id(self, member_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_tenant_member_by_id_endpoint(member_id),
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
        model = TenantMembersGetResultModel(**response.json())
        logger.info(f'Successfully get tenant member by ID.')
        return model

    @allure.step("Get tenant member this.")
    def get_tenant_member_this(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_tenant_member_this_endpoint,
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
        model = TenantMembersGetResultModel(**response.json())
        logger.info(f'Successfully get tenant member this.')
        return model

    @allure.step("Get list tenant members.")
    def get_list_tenant_members(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_tenant_members_endpoint,
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
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list of tenant members.")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}, {data_response}')
        model = TenantMembersListResponseModel(root=response.json())
        logger.info(f'Successfully get list tenant members.')
        return model

    @allure.step("Add tenant member.")
    def post_add_tenant_member(self, account_id: int, user_id: int, invitation_id: str):
        data = {
            "validTill": "2025-05-21T08:39:00.898Z",
            "description": "string",
            "accountID": account_id,
            "userID": user_id,
            "invitationID": invitation_id
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_tenant_members_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_tenant_members_payload(data)
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
            (f'Expected status code {HTTPStatus.CREATED}, '
             f'but got {response.status_code}, {data_response}')
        model = AddTenantMemberResponseModel(results=response.json())
        logger.info(f'Successfully add tenant members.')
        return model

    @allure.step("Update tenant member.")
    def put_update_tenant_member(self, member_id: int):
        model_before = self.get_tenant_member_by_id(member_id)
        data = {
            "validTill": "2025-05-21T08:39:00.898Z",
            "description": "string",
            "id": member_id
        }
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_tenant_members_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_update_tenant_members_payload(data)
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
            (f'Expected status code {HTTPStatus.ACCEPTED}, '
             f'but got {response.status_code}, {data_response}')
        model_after = self.get_tenant_member_by_id(member_id)
        assert model_before.description != model_after.description, \
            f"{model_before.description} is equal {model_after.description}."
        assert model_before.validTill != model_after.validTill, \
            f"{model_before.validTill} is equal {model_after.validTill}."
        logger.info(f'Successfully update tenant member.')
        return None

    @allure.step("Delete tenant members by list.")
    def delete_tenant_members_by_list(self, *member_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.put_update_tenant_members_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_tenant_members_by_list_payload(*member_ids)
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
            (f'Expected status code {HTTPStatus.ACCEPTED}, '
             f'but got {response.status_code}, {data_response}')
        logger.warning(f'Successfully delete tenant members ID {member_ids}.')
        return None

    @allure.step("Get tenant members anonymous user.")
    def get_tenant_members_anonymous_user(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_anonymous_user_this_tenant_endpoint,
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
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list of anonymous user.")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}, {data_response}')
        model = SuccessTenantMembersListResultModel(**response.json())
        logger.info(f'Successfully get tenant members anonymous user.')
        return model
