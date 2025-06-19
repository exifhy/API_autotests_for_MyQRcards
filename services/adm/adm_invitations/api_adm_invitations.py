import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.adm.adm_invitations.payloads import Payloads
from services.adm.adm_invitations.endpoints import Endpoints
from config.headers import Headers
from services.adm.adm_invitations.models.adm_invitations_model import *
import time
from datetime import datetime, timedelta
from http import HTTPStatus
from utils.token_utils import get_token


class AdmInvitationsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Get invitation by id.")
    def get_invitation_by_id(self, invitation_id: str):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_invitation_by_id_endpoint(invitation_id),
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
        model = InvitationsGetResultModel(**response.json())
        logger.info(f'Successfully get invitation by ID {invitation_id}.')
        return model

    @allure.step("Delete invitation by id.")
    def delete_invitation_by_id(self, invitation_id: str):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_invitation_by_id_endpoint(invitation_id),
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
        logger.warning(f'Successfully delete invitation by ID {invitation_id}.')
        return None

    @allure.step("Get short invitation by id.")
    def get_short_invitation_by_id(self, invitation_id: str):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_short_invitation_by_id_endpoint(invitation_id),
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
        model = InvitationsGetShortResultModel(**response.json())
        logger.info(f'Successfully get short invitation by ID {invitation_id}.')
        return model

    @allure.step("Get list invitation.")
    def get_list_invitation(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_invitations_endpoint,
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
            logger.warning(f"Status code:{HTTPStatus.NO_CONTENT}, no list of invitations.")
            return None
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            (f'Expected status code {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, '
             f'but got {response.status_code}, {data_response}')
        model = SuccessGetListInvitationProjectionModel(root=response.json())
        logger.info(f'Successfully get list invitations.')
        return model

    @allure.step("Add invitation.")
    def post_add_invitation(self, user_template_id: int):
        from_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        till_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
        data = {
            "userTemplateID": f"{user_template_id}",
            "description": "Приглашение создано авто-тестом.",
            "allowSelfRegistration": True,
            "validFrom": from_date,
            "validTill": till_date,
            "isPublic": True,
            "allowRegisterWithoutVerification": True,
            "requiredSelfRegistration": True
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_invitations_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_invitations_payload(data)
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
        model = SuccessAddListInvitationsAddResultModel(results=response.json())
        logger.info(f'Successfully add invitation.')
        return model

    @allure.step("Add three invitations.")
    def post_add_three_invitations(self, user_template_id: int):
        from_date = datetime.now().strftime("%Y-%m-%d")
        till_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
        data = {
            "userTemplateID": f"{user_template_id}",
            "description": "Приглашение создано авто-тестом 1.",
            "allowSelfRegistration": True,
            "validFrom": from_date,
            "validTill": till_date,
            "isPublic": False,
            "allowRegisterWithoutVerification": False,
            "requiredSelfRegistration": False
        }
        data2 = {
            "userTemplateID": f"{user_template_id}",
            "description": "Приглашение создано авто-тестом 2.",
            "allowSelfRegistration": False,
            "validFrom": from_date,
            "validTill": till_date,
            "isPublic": True,
            "allowRegisterWithoutVerification": True,
            "requiredSelfRegistration": True
        }
        data3 = {
            "userTemplateID": f"{user_template_id}",
            "description": "Приглашение создано авто-тестом 3.",
            "allowSelfRegistration": True,
            "validFrom": from_date,
            "validTill": till_date,
            "isPublic": False,
            "allowRegisterWithoutVerification": True,
            "requiredSelfRegistration": True
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_invitations_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_invitations_payload(data, data2, data3)
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
        model = SuccessAddListInvitationsAddResultModel(results=response.json())
        logger.info(f'Successfully add three invitations.')
        return model

    @allure.step("Update invitation.")
    def put_update_invitation(self, invitation_id: str, user_template_id: int):
        from_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        till_date = (datetime.now() + timedelta(days=11)).strftime("%Y-%m-%d")
        model_before = self.get_invitation_by_id(invitation_id)
        data = {
            "id": invitation_id,
            "userTemplateID": f"{user_template_id}",
            "description": "Приглашение обновлено авто-тестом",
            "allowSelfRegistration": False,
            "validFrom": from_date,
            "validTill": till_date,
            "isPublic": False,
            "allowRegisterWithoutVerification": False,
            "requiredSelfRegistration": False
        }
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_invitations_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_add_invitations_payload(data)
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
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        model_after = self.get_invitation_by_id(invitation_id)
        assert model_before.description != model_after.description, \
            f"{model_before.description} is equal {model_after.description}."
        assert model_before.allowSelfRegistration != model_after.allowSelfRegistration, \
            f"{model_before.allowSelfRegistration} is equal {model_after.allowSelfRegistration}."
        assert model_before.validFrom != model_after.validFrom, \
            f"{model_before.validFrom} is equal {model_after.validFrom}."
        assert model_before.validTill != model_after.validTill, \
            f"{model_before.validTill} is equal {model_after.validTill}."
        assert model_before.isPublic != model_after.isPublic, \
            f"{model_before.isPublic} is equal {model_after.isPublic}."
        assert model_before.allowRegisterWithoutVerification != model_after.allowRegisterWithoutVerification, \
            f"{model_before.allowRegisterWithoutVerification} is equal {model_after.allowRegisterWithoutVerification}."
        assert model_before.requiredSelfRegistration != model_after.requiredSelfRegistration, \
            f"{model_before.requiredSelfRegistration} is equal {model_after.requiredSelfRegistration}."
        logger.info(f'Successfully update invitation ID {invitation_id}.')
        return None

    @allure.step("Delete invitations by list.")
    def delete_invitations_by_list(self, *invitation_ids: str or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_invitations_by_list_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_invitations_by_list_payload(*invitation_ids)
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
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.warning(f'Successfully delete invitations by list {invitation_ids}.')
        return None
