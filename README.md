# API Autotests — MyQRCards LK

### Инструкция написана для использования на машинах с ОС Windows.

## Описание проекта

Проект предназначен для автоматического тестирования REST API личного кабинета MyQRCards.
Покрывает эндпоинты: accounts, cards, companies, contacts, employees, subscriptions и другие.

## Технологии

- Python 3.13 — основной язык программирования проекта.
- pytest — тестовый фреймворк для написания и выполнения тестов.
- requests — библиотека для взаимодействия с API.
- pydantic v2 — библиотека для валидации ответов от API.
- loguru — библиотека логирования.
- python-dotenv — обработка переменных окружения.
- Allure — инструмент для создания отчётов о тестировании.
- GitHub Actions — CI/CD для автоматического запуска тестов по расписанию.

## Установка и настройка

1. Клонируйте репозиторий:

 - git clone <repo-url>
 - cd <repo-name>

2. Создайте виртуальное окружение и активируйте его:

 - python -m venv .venv
 - .venv/Scripts/activate

3. Установите зависимости:

 - pip install -r requirements.txt

4. Установите Allure:

 - https://allurereport.org/docs/install/

5. Проект использует переменные окружения для конфигурации. Создайте файлы на основе примеров:

 - copy .env.example .env.dev
 - copy .env.example .env.prod
 - copy data/ids.example.json data/ids.dev.json
 - copy data/ids.example.json data/ids.prod.json

   ### Обязательные переменные окружения:
   - LK_JWT= (JWT токен личного кабинета для dev)
   - LK_JWT_PROD= (JWT токен личного кабинета для prod)
   - APP_ID= (X-APPLICATION-ID, одинаковый для dev/prod)
   - ACCOUNT_ACTIONS_BASIC_PASSWORD= (пароль для AccountActions тестов)

   ### Обязательные поля в ids.json:
   - host — базовый URL API
   - lk_account_id — ID аккаунта
   - subscription_id — ID подписки
   - company_id_create — ID компании для тестов

## Запуск тестов

1. Для запуска всех тестов на dev или prod:

 - ENVIRON=dev .venv/Scripts/pytest tests/ --env=dev -v
 - ENVIRON=prod .venv/Scripts/pytest tests/ --env=prod -v

2. Для запуска только smoke-тестов:

 - ENVIRON=dev .venv/Scripts/pytest tests/ --env=dev -m smoke -v

3. Для запуска только e2e-тестов:

 - ENVIRON=dev .venv/Scripts/pytest tests/e2e/ --env=dev -v

4. Для параллельного запуска тестов (ускорение):

 - ENVIRON=dev .venv/Scripts/pytest tests/ --env=dev -n auto

5. Для повторного запуска одного теста несколько раз:

 - ENVIRON=dev .venv/Scripts/pytest tests/path/to/test.py --env=dev --count=3

6. Для запуска сценария N раз подряд (проверка стабильности):

 - ENVIRON=dev .venv/Scripts/pytest tests/e2e/test_script_runs.py --env=dev --runs=5 -v

7. Для генерации отчёта Allure (локально):

 - ENVIRON=dev .venv/Scripts/pytest tests/ --env=dev --alluredir=allure-results
 - allure generate allure-results -o allure-report --clean
 - allure open allure-report

8. Для локального накопления истории запусков в Allure-отчёте (запускать тесты с параметром --report=true):

 - ENVIRON=dev .venv/Scripts/pytest tests/ --env=dev --report=true

   При наличии предыдущего отчёта (allure-report/history) история автоматически копируется в allure-results и генерируется новый отчёт.

## Структура проекта

```
services/        — API-клиенты по доменам (accounts, cards, companies, ...)
src/             — хелперы, модели, утилиты, waiter-функции
testkit/         — pytest-фикстуры
tests/api/       — unit/api тесты (проверка конкретных ручек)
tests/e2e/       — e2e flow тесты (create → verify → delete)
config/          — конфигурация окружений и заголовков
data/            — шаблоны ids (секреты не хранятся в репо)
scripts/         — вспомогательные скрипты (Telegram уведомления)
```

## CI/CD — GitHub Actions

Allure-отчёты публикуются на GitHub Pages после каждого прогона.
Результаты отправляются в Telegram.

## Зависимости

Полный список зависимостей можно найти в requirements.txt.
