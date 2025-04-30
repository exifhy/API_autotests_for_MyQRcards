from datetime import datetime, timedelta, UTC
import os
import allure
import pytest
import json
import shutil
import subprocess
from allure_commons.types import AttachmentType
from loguru import logger
from config.headers import Headers
from dotenv import load_dotenv, set_key, unset_key
import requests
import re
import traceback
from utils.helper import Helper
from config.config import HOST, ENVIRON


load_dotenv()


# Определение HOST на основе переменной окружения ENVIRON
# ENVIRON = os.environ.get("ENVIRON", "prod")  # Если STAGE не задан, используем "prod" по умолчанию
# HOST = os.getenv('URL_DEV_HUBEX') if ENVIRON == 'qa' else os.getenv('URL_PROD_HUBEX')
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
API_USER_TOKEN = os.getenv('API_USER_TOKEN')
BASIC_TOKEN = os.getenv('SECOND_BASIC_TOKEN')
POWER_USER_TOKEN = os.getenv('POWER_USER_TOKEN')
TENANT_ID = os.getenv('TENANT_ID')
TENANT_MEMBER_ID = os.getenv('TENANT_MEMBER_ID')
APP_ID = os.getenv('APP_ID')
TOKEN_EXPIRATION_TIME = datetime.min.replace(tzinfo=UTC)
BEARER_TOKEN = None


@allure.step("Authorization via API by Email | Password.")
@pytest.fixture(scope='module')
def bearer_token():
    try:
        response_authentication = requests.post(
            url=f'{HOST}/AUTHN/accounts/login',
            headers=Headers.authentication_header(token=BASIC_TOKEN, app_id=APP_ID)
        )
        logger.info("Send basic token")
        if response_authentication.status_code != 200:
            logger.error(response_authentication.status_code)

        response_authorization_data = response_authentication.json()
        bearer_token = response_authorization_data['access_token']

        response_authorization = requests.post(
            url=f"{HOST}/AUTHZ/accounts/authorize",
            headers=Headers.authorization_header(bearer_token, APP_ID),
            json={
                "tenantID": TENANT_ID,
                "tenantMemberID": TENANT_MEMBER_ID
            }
        )
        logger.info("Tenant authorization by user.")
        if response_authorization.status_code != 200:
            logger.error(response_authorization.status_code)
        response_authorization_data = response_authorization.json()
        token = response_authorization_data['access_token']
        logger.info(f"Return bearer token {token}")
        return token

    except (requests.exceptions.RequestException, TypeError) as er:
        logger.error(er)


@allure.step("Authorization API by cross tenant admin (power user).")
@pytest.fixture(scope='module')
def bearer_token_power_user():
    try:
        response_authentication = requests.post(
            url=f'{HOST}/AUTHN/accounts/login',
            headers=Headers.authentication_header(token=POWER_USER_TOKEN, app_id=APP_ID)
        )
        logger.info("Send basic token")
        if response_authentication.status_code != 200:
            logger.error(response_authentication.status_code)

        response_authorization_data = response_authentication.json()
        token = response_authorization_data['access_token']

        response_authorization = requests.post(
            url=f"{HOST}/AUTHZ/accounts/authorize",
            headers=Headers.authorization_header(token, APP_ID),
            json={
                "tenantID": TENANT_ID,
                "tenantMemberID": TENANT_MEMBER_ID
            }
        )
        logger.info("Tenant authorization by power user.")
        if response_authorization.status_code != 200:
            logger.error(response_authorization.status_code)
        response_authorization_data = response_authorization.json()
        token_bearer = response_authorization_data['access_token']
        logger.info(f"Return bearer token {token_bearer}")
        return token_bearer

    except (requests.exceptions.RequestException, TypeError) as er:
        logger.error(er)


@pytest.fixture
def return_func_name():
    return return_func_name_with_error


def return_func_name_with_error() -> str:
    # Получаем traceback в виде строки
    tb = traceback.format_exc()

    # Находим все функции в стеке вызовов
    matches = re.findall(r'File .+?, line \d+, in (\w+)', tb)

    # Возвращаем последнюю найденную функцию, так как ошибка произошла в ней
    return matches[-1] if matches else "Unknown function"


@allure.title("Get API user access token.")
def get_api_user_access_token():
    global TOKEN_EXPIRATION_TIME, BEARER_TOKEN
    now = datetime.now(UTC)
    if BEARER_TOKEN and TOKEN_EXPIRATION_TIME and now < TOKEN_EXPIRATION_TIME:
        return BEARER_TOKEN

    try:
        response_authorization = requests.post(
            url=f"{HOST}/AUTHZ/AccessTokens/",
            headers=Headers.basic_content_type,
            json={
                "serviceToken": API_USER_TOKEN,
            }
        )
        if response_authorization.status_code != 200:
            logger.error(f'{response_authorization.status_code}: {response_authorization.text}')
            return None

        response_authorization_data = response_authorization.json()
        BEARER_TOKEN = response_authorization_data['access_token']
        TOKEN_EXPIRATION_TIME = now + timedelta(minutes=25)
        # set_key('.env', 'API_TOKEN', BEARER_TOKEN)
        # os.environ["API_TOKEN"] = BEARER_TOKEN
        return BEARER_TOKEN
    except (requests.exceptions.RequestException, TypeError) as er:
        logger.error(er)
        return None


@allure.step("Вызывается перед выполнением тестов.")
def pytest_sessionstart(session):
    """Вызывается перед выполнением тестов."""
    logger.debug("pytest_session start called")
    token = get_api_user_access_token()
    if token:
        cache = session.config.cache
        cache.set("api_token", token)
        logger.debug("Cache set for api_token")
        set_key('.env', 'API_TOKEN', token)
        logger.debug('Token set in .env file')
        os.environ["API_TOKEN"] = token
        print(f"::set-output name=API_TOKEN::{token}")    # Экспорт токена


@allure.step("SYSTEM check of access token lifetime before each test.")
def pytest_runtest_setup(item):
    """Проверка перед каждым тестом."""
    global TOKEN_EXPIRATION_TIME, BEARER_TOKEN

    load_dotenv()

    cache = item.config.cache
    cached_token = cache.get("api_token", None)

    if cached_token:
        BEARER_TOKEN = cached_token
        logger.debug("Loaded API token from pytest cache")

    Helper.attach_token_expiration_time(TOKEN_EXPIRATION_TIME)
    now = datetime.now(UTC)
    Helper.attach_test_start_time(now)

    if now > TOKEN_EXPIRATION_TIME:
        logger.debug("Token expired, refreshing...")
        new_token = get_api_user_access_token()
        Helper.attach_token(new_token)
        if new_token:
            cache.set("api_token", new_token)  # Обновляем кэш
            set_key('.env', 'API_TOKEN', new_token)  # Обновляем .env
            os.environ["API_TOKEN"] = new_token  # Обновляем переменные окружения
            logger.debug(f"New token set in pytest cache and .env - {os.environ["API_TOKEN"]}")
            print(f"::set-output name=API_TOKEN::{new_token}")


def pytest_sessionfinish(session, exitstatus):
    """Вызывается после выполнения тестов."""
    logger.debug("pytest_sessionfinish called")
    unset_key('.env', 'API_TOKEN')
    logger.debug("API_TOKEN unset in .env file")


@allure.step("Attach host information")
@pytest.fixture(autouse=True, scope='session')
def attach_host_info():
    info = {
        "STAGE": ENVIRON,
        "HOST": HOST,
        "TENANT ID": TENANT_ID
    }
    allure.attach(body=json.dumps(info, indent=4), name='Host Info', attachment_type=AttachmentType.JSON)


def pytest_addoption(parser):
    parser.addoption(
        "--report", action="store", default="false", help="Run fixture if --report=true"
    )
    parser.addoption(
        "--runs",
        action="store",
        default=1,
        help="Number of times to run the test scenario"
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
