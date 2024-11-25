import allure
import requests
from loguru import logger
from requests import JSONDecodeError
from utils.helper import Helper
from services.es.es_asset_skills.payloads import Payloads
from services.es.es_asset_skills.endpoints import Endpoints
from config.headers import Headers
from services.es.es_asset_skills.models.es_asset_skills_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class EsAssetSkillsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Add skills to assets.")
    def post_add_skills_to_one_asset(self, asset_id: int, *skill_id: int):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_skills_to_assets_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.skills_and_one_asset_payload(
                asset_id, *skill_id
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
        model = SuccessAddSkillsToAssetsResultModel(result=response.json())
        logger.info(f'Successfully add skills with ID: {skill_id} to asset with ID: {asset_id}.')
        return model

    @allure.step("Delete skills from one asset.")
    def delete_skills_from_one_asset(self, asset_id: int, *skill_id: int):
        start = time.time()
        response = requests.delete(
            url=self.endpoints.delete_skills_from_assets_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.skills_and_one_asset_payload(
                asset_id, *skill_id
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
        logger.warning(f'Successfully delete skills from asset with ID: {asset_id}, skills ID: {skill_id}.')
