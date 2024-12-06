import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.es.es_asset_template_skills.payloads import Payloads
from services.es.es_asset_template_skills.endpoints import Endpoints
from config.headers import Headers
from services.es.es_asset_template_skills.models.es_asset_template_skills_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class EsAssetTemplateSkillsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add skills to asset templates.")
    def post_skills_to_asset_templates(self, asset_template_id: int, skill_id: int):
        skills = {
            "skillID": skill_id,
            "isOptional": True
        }
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_skills_to_asset_templates_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_add_skills_to_asset_templates_payload(asset_template_id, skills)
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.CREATED, \
            f'Code:{response.status_code}.Message:{response.json()}'
        model = SuccessAddSkillsToAssetTemplatesModel(result=response.json())
        logger.info(f'Successfully add skills with ID: {skill_id} to templates with ID: {asset_template_id}.')
        return model

    @allure.step("Delete skills from asset templates.")
    def delete_skills_from_asset_templates(self, asset_template_id: int, *skill_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_skills_from_asset_templates_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_skills_from_asset_templates_payload(asset_template_id, *skill_ids)
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Code:{response.status_code}.Message:{response.json()}'
        logger.warning(f'Successfully delete skills with ID: {skill_ids} from templates with ID: {asset_template_id}.')

    @allure.step("Delete skills from asset template by Id.")
    def delete_skills_from_asset_template_by_id(self, asset_template_id: int, *skill_ids: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_skills_from_asset_template_by_id_endpoint(asset_template_id),
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.delete_skills_from_asset_template_by_id_payload(*skill_ids)
        )
        end = time.time()
        try:
            self.attach_response(response.json())
        except JSONDecodeError:
            logger.warning("Received response is not a valid JSON")
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        self.attach_time(start, end)
        self.attach_url(response.request.url)
        self.attach_request(response.request.body)
        assert response.status_code == HTTPStatus.ACCEPTED, \
            f'Code:{response.status_code}.Message:{response.json()}'
        logger.warning(f'Successfully delete skills with ID: {skill_ids} from template with ID: {asset_template_id}.')
