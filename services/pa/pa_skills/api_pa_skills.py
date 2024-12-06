import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.pa.pa_skills.payloads import Payloads
from services.pa.pa_skills.endpoints import Endpoints
from config.headers import Headers
from services.pa.pa_skills.models.pa_skills_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os
from random import randint

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class PaSkillsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add skills to this tenant.")
    def post_add_skills_to_tenant(self):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_skills_for_tenant_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_add_skills_for_tenant_payload(
                (f'Навык-{randint(100, 199)}', f'Описание-{randint(100, 199)}', True)
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}, {response.json()}'
        model = SuccessAddSkillsModel(skills=response.json())
        logger.info(f'Successfully add skills with ID: {model.skills[0].skillID}.')
        return model

    @allure.step("Add three skills to this tenant.")
    def post_add_three_skills_to_tenant(self):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_skills_for_tenant_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_add_skills_for_tenant_payload(
                (f'Навык-{randint(100, 199)}', f'Описание-{randint(100, 199)}', True),
                (f'Навык-{randint(100, 199)}', f'Описание-{randint(100, 199)}', True),
                (f'Навык-{randint(100, 199)}', f'Описание-{randint(100, 199)}', True),
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, f'Status code {response.status_code}, {response.json()}'
        model = SuccessAddSkillsModel(skills=response.json())
        logger.info(f'Successfully add skills with ID: '
                    f'{model.skills[0].skillID}, {model.skills[1].skillID}, {model.skills[2].skillID}.')
        return model

    @allure.step("Delete skills by list.")
    def delete_skills_by_list(self, *args):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_skills_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_skills_by_list_payload(*args)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.warning(f'Successfully delete skills by list with ID: {args}.')

    @allure.step("Get the list of skills for the given tenant.")
    def get_list_skills_tenant(self):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_skills_for_tenant_endpoint,
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
        assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
            f'Status code {response.status_code}, {response.json()}'
        model = SuccessGetSkillsListResultModel(root=response.json())
        logger.info(f'Successfully get the list of skills for the given tenant.')
        return model

    @allure.step("Get the list of skills for the given tenant and return first.")
    def get_list_skills_tenant_return_first_skills(self):
        params = {
            "isDeleted": False
        }
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_list_skills_for_tenant_endpoint, params=params,
            headers=self.headers.basic_header(API_TOKEN)
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
            self.attach_response_headers(response.headers)
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        if response.status_code == HTTPStatus.NO_CONTENT:
            logger.warning('No skills found. Creating a skill.')
            model_skill = self.post_add_skills_to_tenant()
            return model_skill.skills[0].skillID
        else:
            assert response.status_code in {HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT}, \
                f'Status code {response.status_code}, {response.json()}'
            model = SuccessGetSkillsListResultModel(root=response.json())
            for key, skill in model.root.items():
                logger.info(f'Successfully get a list skills.')
                logger.info(f"Skill ID: {key}, Name: {skill.name}")
                return int(key)

    @allure.step("Update skills to this tenant.")
    def put_update_skills_to_tenant(self, skill_id: int):
        start = time.time()
        response = requests.put(
            url=self.endpoints.put_update_skills_for_tenant_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.put_update_skills_for_tenant_payload(
                (skill_id, f'Обновленный-{randint(1, 99)}', f'Обновленное-{randint(1, 99)}', False)
            )
        )
        end = time.time()
        logger.info(response.headers)
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, f'Status code {response.status_code}, {response.json()}'
        logger.info(f'Successfully update skills to this tenant with ID: {skill_id}.')

    @allure.step("Get skill by ID.")
    def get_skill_by_id(self, skill_id: int):
        start = time.time()
        response = requests.get(
            url=self.endpoints.get_skill_by_id(skill_id),
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
        assert response.status_code == HTTPStatus.OK, \
            f'Status code {response.status_code}, {response.json()}'
        model = SuccessGetSkillByIdResultModel(**response.json())
        logger.info(f'Successfully get skill by ID: {skill_id}.')
        return model

    @allure.step("Delete skill by ID.")
    def delete_skill_by_id(self, skill_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_skill_by_id(skill_id),
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
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Status code {response.status_code}, {response.json()}'
        logger.warning(f'Successfully delete skill by ID: {skill_id}.')
