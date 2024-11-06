import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.es.es_asset_list_queries.payloads import Payloads
from services.es.es_asset_list_queries.endpoints import Endpoints
from config.headers import Headers
from services.es.es_asset_list_queries.models.es_asset_list_queries_model import *
import time
from http import HTTPStatus
from dotenv import load_dotenv
import os


load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


class EsAssetListQueriesAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Creates a saved queries and binds it to the current user.")
    def post_add_queries_binds_to_user(self):
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_add_queri_endpoint,
            headers=self.headers.basic_header(API_TOKEN),
            json=self.payloads.post_add_queries_binds_to_user_payload()
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.ACCEPTED, f'{response.status_code},{response.json()}'
        model = SuccessAddAssetListQueryModel(**response.json())
        logger.info(f'Successfully creates a saved queries and binds it to the current user.')
        return model
