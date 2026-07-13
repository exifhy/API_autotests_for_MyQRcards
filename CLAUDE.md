# API Autotests — MyQRCards (LK)

@docs/FIXES_LOG.md
@docs/SERVICES.md
@docs/CI_CD.md

## Что это

Проект автотестов для API личного кабинета MyQRCards. Тесты на Python + pytest + allure.

## Два remote репозитория

| Remote | URL | Назначение |
|---|---|---|
| `origin` | github.com/exifhy/API_autotests_for_MyQRcards | CI/CD, Allure отчёты, Telegram уведомления |
| `azure` | dev.azure.com/melston/MyQRcards/_git/MyQrCard.Test.Api | Корпоративное хранилище кода |

### Важно при пуше в Azure

**`.github/` папку НЕ пушить в Azure.**

```bash
# GitHub — напрямую
git push origin main

# Azure — через ветку и PR (main защищён)
git push azure HEAD:feature/название-ветки
```

После создания PR в Azure → Complete merge → код попадает в main.

### Процесс добавления новых тестов
1. Написать тест локально
2. Закоммитить
3. `git push origin main`
4. `git push azure HEAD:feature/название`
5. Создать PR в Azure DevOps → Complete merge

## Структура проекта

```
services/          — API-клиенты по доменам (companies, contacts, accounts, subscriptions, ...)
src/               — утилиты, хелперы, конфиги, модели
testkit/fixtures/  — pytest-фикстуры (company.py, employee.py, ...)
tests/api/         — unit/api тесты (проверка конкретных ручек)
tests/e2e/         — e2e flow тесты (create → verify → delete)
config/            — конфигурация окружений
```

## Архитектурный паттерн

### HTTP-вызовы в сервисах

Все сервисы наследуют `Helper` и делают запросы через `self._call()`:

```python
class SomeAPI(Helper):
    def some_method(self) -> SomeModel:
        response = self._call(
            "GET",
            url=self.endpoints.some_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.OK, ...
        return SomeModel(**response.json())
```

`_call` автоматически: выставляет `timeout=30`, прикрепляет к Allure время ответа, URL, тело.

### HTTP-вызовы вне сервисов (conftest, helpers, waiter-функции)

```python
from src.support.helper import Helper

_helper = Helper()

def _wait_something_deleted(resource_id: int) -> bool:
    def _gone():
        response = _helper._call("GET", url=f"{host}/{resource_id}", headers=headers)
        return True if response.status_code in (HTTPStatus.NOT_FOUND, HTTPStatus.CONFLICT) else None
    return bool(wait_until(_gone, timeout_s=60, step_s=3))
```

**Правило:** `requests.get/post/delete` напрямую — запрещено. Только через `_call()`.

### e2e flow тесты — шаблон

```python
def test_some_flow(self, lk_api, cfg):
    resource_id = None
    try:
        with allure.step("01. POST ..."):
            resource_id = ...
        with allure.step("02. DELETE ..."):
            ...
            resource_id = None  # сбрасываем, чтобы finally не чистил повторно
    finally:
        if resource_id:
            try:
                lk_api.delete(f"/resource/{resource_id}")
            except Exception:
                pass
```

**Правила:**
- `assert` в `finally` — антипаттерн
- `finally` всегда молчит (`try/except pass`)
- Проверка удаления компании — через `GET /companies` (список), не по ID

### Модели

- `extra="allow"` (`BaseModel`) — для нестабильных/публичных ответов (cardAttributes, cardlinks)
- `extra="forbid"` (`StrictBaseModel`) — для стабильных LK ответов
- При появлении нового поля в StrictBaseModel → добавить `field: Optional[type] = None`

### Waiter-функции после DELETE

API может возвращать `409 Conflict` с `code: "NotFound"` вместо `404`. Всегда принимать оба:
```python
if response.status_code in (HTTPStatus.NO_CONTENT, HTTPStatus.NOT_FOUND, HTTPStatus.CONFLICT):
    return True
```

## Токены и авторизация

- `LK_JWT` — токен для всех операций через `lk_api`
- `EXPIRED_JWT` — JWT аккаунта с истёкшей подпиской (для тестов AllData=true, REQUIREMENT 30709)
- Компании, созданные через `API_TOKEN`, нельзя удалить через `LK_JWT` → 403
- **Решение:** тесты создают и удаляют свои ресурсы сами
- Для запуска на prod: `ENVIRON=prod pytest --env=prod` — переменная до старта pytest
- `get_expired_jwt()` из `src/support/token_utils.py` — читает `EXPIRED_JWT` из env

## Полезные команды

```bash
# Запуск всех тестов
pytest --env=dev -v

# Только smoke
pytest --env=dev -m smoke -v

# Конкретный файл
pytest tests/e2e/company/test_company_create_get_delete_flow.py -v

# На prod
ENVIRON=prod pytest --env=prod -v

# С allure
pytest --env=dev --alluredir=allure-results
allure generate allure-results -o allure-report --clean
allure open allure-report

# Через venv напрямую
ENVIRON=dev .venv/Scripts/pytest tests/ -v
```

## Замечания

- `.env.dev` и `.env.prod` содержат токены — в git не коммитить
- Количество тестов: 388 (api: 132 файла, e2e: 43 файла)
- `.tmp_postman_items_new.txt` — список ручек из Postman, для справки
- `expired_cardlink_id` в `ids.dev.json` / `ids.prod.json` — токен карт-линка с истёкшей подпиской (нужен для тестов AllData=true)
- `unbound_cardlink_id` в `ids.dev.json` / `ids.prod.json` — токен кардлинка, не привязанного к аккаунту (нужен для тестов IsSkipCheck, REQUIREMENT 31202)

## Закомментированные тесты (раскомментировать при наличии данных)

| Файл | Тест | Причина |
|---|---|---|
| `tests/api/accounts/test_accounts_sso_bindings.py` | `test_sso_bindings_structure` | Тест-аккаунт не имеет привязанных SSO — всегда 204. Раскомментировать когда на dev-аккаунте будет привязан VK ID или Яндекс ID. |
