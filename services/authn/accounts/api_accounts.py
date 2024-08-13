import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.authn.accounts.payloads import Payloads
from services.authn.accounts.endpoints import Endpoints
from config.headers import Headers
from services.authn.accounts.models.accounts_model import *
import time
from http import HTTPStatus


class AccountsAPI(Helper):

    def __init__(self):
        super().__init__()
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.headers = Headers()

