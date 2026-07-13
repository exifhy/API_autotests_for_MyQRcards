from datetime import timedelta
from services.adm.users.api_adm_users import AdmUsersAPI
import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.pa.pa_user_skills.payloads import Payloads
from services.pa.pa_user_skills.endpoints import Endpoints
from config.headers import Headers
from services.pa.pa_user_skills.models.pa_user_skills_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class PaUserSkillsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()
        self.api_adm_users = AdmUsersAPI()

    @allure.step("Add skills to user.")
    def post_add_skills_to_user(self, user_id: int, skill_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_user_skills_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.post_user_skills_payload(user_id, skill_id)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response_headers(response.headers)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Expected status code {HTTPStatus.CREATED}, but got {response.status_code}, {data_response}'
        model = UserSkillsListResponseModel(results=response.json())
        logger.info(f'Successfully add skills with ID {skill_id} to user ID {user_id}.')
        return model

    @allure.step("Update user skills.")
    def put_update_user_skills(self, user_id: int, skill_id: int):
        model_before = self.api_adm_users.get_user_skills_by_user_id(user_id)
        from_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_user_skills_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.put_user_skills_payload(user_id, skill_id, from_date)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response_headers(response.headers)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        model_after = self.api_adm_users.get_user_skills_by_user_id(user_id)
        assert model_before != model_after, "User skills not updated."
        logger.info(f'Successfully update user skills, with ID {skill_id}, user ID {user_id}.')

    @allure.step("Delete skills from user.")
    def delete_skills_from_user(self, user_id: int, *skill_ids: int or tuple):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_user_skills_endpoint,
            headers=self.headers.basic_header(get_token()),
            json=self.payloads.delete_skills_from_user_payload(user_id, *skill_ids)
        )
        end = time.time()
        logger.info(response.headers)
        data_response = self.response_content(response)
        self.attach_response_headers(response.headers)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Expected status code {HTTPStatus.ACCEPTED}, but got {response.status_code}, {data_response}'
        logger.warning(f'Successfully delete skills ID {skill_ids} from user ID {user_id}.')
