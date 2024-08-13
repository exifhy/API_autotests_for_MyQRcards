import os
import allure
import pytest
import json
from allure_commons.types import AttachmentType
import base64
import urllib.parse


# Определение HOST на основе переменной окружения ENVIRON
ENVIRON = os.environ.get("ENVIRON", "prod")  # Если STAGE не задан, используем "prod" по умолчанию
HOST = "https://dev-api.hubex.ru/fsm" if ENVIRON == 'qa' else "https://api.hubex.ru/fsm"


@allure.step("Attach host information")
@pytest.fixture(autouse=True, scope='session')
def attach_host_info():
    info = {
        "STAGE": ENVIRON,
        "HOST": HOST
    }
    allure.attach(body=json.dumps(info, indent=4), name='Host Info', attachment_type=AttachmentType.JSON)


def basic_token_generation(login: str, password: str) -> str:
    # Используем аналог encodeURIComponent для кодирования логина и пароля
    encoded_login = urllib.parse.quote(login, safe='')
    encoded_password = urllib.parse.quote(password, safe='')

    # Формируем строку логин:пароль
    credentials = f"{encoded_login}:{encoded_password}"

    # Кодируем строку в base64
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

    return encoded_credentials
