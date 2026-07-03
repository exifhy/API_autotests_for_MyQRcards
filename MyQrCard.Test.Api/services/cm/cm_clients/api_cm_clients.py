import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.cm.cm_clients.payloads import Payloads
from services.cm.cm_clients.endpoints import Endpoints
from config.headers import Headers
from services.cm.cm_clients.models.cm_clients_model import *
import time
from http import HTTPStatus
from datetime import datetime, timezone


class CmClientsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

    @allure.step("Saves location data.")
    def post_clients_locations(self):
        client_id = "fe3ec3a4-3f3a-55f3-8868-ef2ff30f184f"
        now_utc = datetime.now(timezone.utc)
        date = now_utc.isoformat(timespec='milliseconds').replace("+00:00", "Z")   
        start = time.time()
        response = requests.post(
            url=self.endpoints.post_clients_locations_endpoint,
            json=self.payloads.post_clients_locations_payloads(date),
            headers=self.headers.header_for_client_locations(client_id, "180")
        )
        end = time.time()
        logger.info(response.headers)
        self.attach_response_headers(response.headers)
        data_response = self.response_content(response)
        self.attach_response(data_response)
        self.attach_time(start, end)
        self.attach_request(response.request.body)
        self.attach_url(response.request.url)
        assert response.status_code == HTTPStatus.OK, \
            f'Expected status code{HTTPStatus.OK}, but got {response.status_code}, {data_response}'
        model = SuccessAddClientsLocationsModel(**response.json())
        logger.info(f'Successfully add location to client.')
        return model