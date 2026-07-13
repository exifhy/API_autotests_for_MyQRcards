import allure
import requests
from loguru import logger
from utils.helper import Helper
from services.adm.adm_role_attachments.payloads import Payloads
from services.adm.adm_role_attachments.endpoints import Endpoints
from config.headers import Headers
from services.adm.adm_role_attachments.models.adm_role_attachments_model import *
import time
from http import HTTPStatus
from utils.token_utils import get_token


class AdmRoleAttachmentsAPI(Helper):
    ...

