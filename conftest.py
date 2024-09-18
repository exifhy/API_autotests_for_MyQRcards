import os
import allure
import pytest
import json
import shutil
import subprocess
from allure_commons.types import AttachmentType
from loguru import logger
from requests import JSONDecodeError

from config.headers import Headers
from dotenv import load_dotenv, set_key, unset_key
import requests


load_dotenv()


# Определение HOST на основе переменной окружения ENVIRON
ENVIRON = os.environ.get("ENVIRON", "prod")  # Если STAGE не задан, используем "prod" по умолчанию
HOST = os.getenv('URL_DEV_HUBEX') if ENVIRON == 'qa' else os.getenv('URL_PROD_HUBEX')
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
API_USER_TOKEN = os.getenv('API_USER_TOKEN')


def get_api_user_access_token():
    try:
        response_authorisation = requests.post(
            url=f"{HOST}/AUTHZ/AccessTokens/",
            headers=Headers.basic_content_type,
            json={
                "serviceToken": API_USER_TOKEN,
            }
        )
        if response_authorisation.status_code != 200:
            logger.error(response_authorisation.status_code)
        # try:
        #     logger.warning(response_authorisation.json())
        # except JSONDecodeError:
        #     logger.warning("Received response is not a valid JSON")
        response_authorisation_data = response_authorisation.json()
        bearer_token = response_authorisation_data['access_token']
        return bearer_token
    except (requests.exceptions.RequestException, TypeError) as er:
        logger.error(er)


def pytest_sessionstart(session):
    """Вызывается перед выполнением тестов."""
    logger.info("pytest_session start called")
    token = get_api_user_access_token()
    cache = session.config.cache
    cache.set("api_token", token)
    logger.info("Cache set for api_token")
    set_key('.env', 'API_TOKEN', token)
    logger.info('Token set in .env file')
    os.environ["API_TOKEN"] = token
    print(f"::set-output name=API_TOKEN::{token}")    # Экспорт токена


def pytest_sessionfinish(session, exitstatus):
    """Вызывается после выполнения тестов."""
    logger.info("pytest_sessionfinish called")
    unset_key('.env', 'API_TOKEN')
    logger.info("API_TOKEN unset in .env file")


@allure.step("Attach host information")
@pytest.fixture(autouse=True, scope='session')
def attach_host_info():
    info = {
        "STAGE": ENVIRON,
        "HOST": HOST
    }
    allure.attach(body=json.dumps(info, indent=4), name='Host Info', attachment_type=AttachmentType.JSON)


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
