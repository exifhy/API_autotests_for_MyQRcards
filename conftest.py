import os
import allure
import pytest
import json
import shutil
import subprocess
from allure_commons.types import AttachmentType
import base64
import urllib.parse
from loguru import logger

# Определение HOST на основе переменной окружения ENVIRON
ENVIRON = os.environ.get("ENVIRON", "prod")  # Если STAGE не задан, используем "prod" по умолчанию
HOST = "https://dev-api.hubex.ru/fsm" if ENVIRON == 'qa' else "https://api.hubex.ru/fsm"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


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


def pytest_addoption(parser):
    parser.addoption(
        "--report", action="store", default="false", help="Run fixture if --report=true"
    )


@pytest.fixture(scope="session", autouse=True)
def setup_allure_history_fixture(request):
    if request.config.getoption("--report") == "true":
        request.addfinalizer(setup_allure_history)


def setup_allure_history():
    try:
        # logger.info('Start generate history')
        # Путь к папке allure-report/history
        allure_report_history = os.path.join(ROOT_DIR, 'allure-report', 'history')

        # Проверка наличия папки allure-report/history
        if os.path.exists(allure_report_history):
            # Содержание папки allure-report/history
            history_files = os.listdir(allure_report_history)

            # Путь к папке allure-results
            allure_results_dir = os.path.join(ROOT_DIR, 'allure-results')

            # Проверка наличия папки allure-results
            if os.path.exists(allure_results_dir):
                # Путь к папке allure-results/history
                allure_results_history = os.path.join(allure_results_dir, 'history')

                # Создание папки allure-results/history, если она не существует
                os.makedirs(allure_results_history, exist_ok=True)

                # Копирование содержимого из allure-report/history в allure-results/history
                for file_name in history_files:
                    full_file_name = os.path.join(allure_report_history, file_name)
                    if os.path.isfile(full_file_name):
                        shutil.copy(full_file_name, allure_results_history)
                    # logger.info('Copy history complete')

        # Выполнение команды "allure generate allure-results --clean"
        allure_path = os.path.join(os.environ['USERPROFILE'], 'scoop', 'shims', 'allure.cmd')
        subprocess.run([allure_path, 'generate', 'allure-results', '--clean'], check=True)

    except FileNotFoundError as err:
        logger.error(err)
