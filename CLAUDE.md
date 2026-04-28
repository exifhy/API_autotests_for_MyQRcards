# API Autotests — MyQRCards (LK)

## Что это

Проект автотестов для API личного кабинета MyQRCards. Тесты на Python + pytest + allure.

## Структура проекта

```
services/          — API-клиенты по доменам (companies, contacts, accounts, subscriptions, ...)
src/               — утилиты, хелперы, конфиги, модели
testkit/fixtures/  — pytest-фикстуры (company.py, employee.py, ...)
tests/api/         — unit/api тесты (проверка конкретных ручек)
tests/e2e/         — e2e flow тесты (create → verify → delete)
config/            — конфигурация окружений
```

## Архитектурный паттерн (принятый стандарт)

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

`_call` автоматически:
- выставляет `timeout=30`
- прикрепляет к allure: время ответа, URL запроса, тело ответа

`CompaniesBaseAPI._request` тоже использует `_call` внутри — все компании-сервисы получают timing автоматически.

### HTTP-вызовы вне сервисов (conftest, helpers, waiter-функции)

В файлах, которые не являются сервисами (conftest.py, helpers.py, waiter-функции), используется модульный инстанс `_helper`:

```python
from src.support.helper import Helper

_helper = Helper()

def _wait_something_deleted(resource_id: int) -> bool:
    def _gone():
        response = _helper._call("GET", url=f"{host}/{resource_id}", headers=headers)
        return True if response.status_code == HTTPStatus.NOT_FOUND else None
    return bool(wait_until(_gone, timeout_s=60, step_s=3))
```

**Правило:** `requests.get/post/delete` напрямую в тестах и хелперах — запрещено. Только через `_call()` — иначе вызов не попадает в Allure.

### e2e flow тесты

Все e2e flow тесты пишутся по шаблону **один метод + try/finally**:

```python
def test_some_flow(self, lk_api, cfg):
    resource_id = None
    try:
        with allure.step("01. POST ..."):
            ...
            resource_id = ...

        with allure.step("02. GET ..."):
            ...

        with allure.step("03. DELETE ..."):
            ...
            resource_id = None  # ← сбрасываем, чтобы finally не чистил повторно

    finally:
        if resource_id:
            try:
                lk_api.delete(f"/resource/{resource_id}")
            except Exception:
                pass
```

**Правила:**
- `assert` в `finally` — антипаттерн, заменяет настоящую ошибку теста
- `resource_id = None` после успешного DELETE — защита от двойной очистки
- `finally` всегда молчит (только `try/except pass`)
- Проверка удаления компании — через `GET /companies` (список), не через `GET /companies/{id}`
- Таймаут ожидания удаления компании — 120s, шаг 5s

## Токены и авторизация

- `LK_JWT` — токен для всех операций через `lk_api` (LkApiClient)
- Компании, созданные через `API_TOKEN` (сервисный аккаунт), нельзя удалить через `LK_JWT` → возвращает 403
- **Решение:** тесты создают и удаляют свои ресурсы сами (не используют заранее созданные чужим токеном)
- Для запуска на prod: `ENVIRON=prod pytest --env=prod` — переменная должна быть выставлена ДО старта pytest (иначе `config.py` возьмёт dev HOST)

## Что было пофиксено

### 403 при удалении компаний
**Проблема:** company_id=3769 был создан под другим токеном (API_TOKEN), LK_JWT не мог его удалить.  
**Фикс:** Переписаны тесты — каждый создаёт свою компанию и удаляет её же.

### assert в finally (антипаттерн)
**Проблема:** `assert gone is True` в teardown фикстуры маскировал настоящую ошибку теста.  
**Фикс:** `testkit/fixtures/company.py` — `_safe_delete_company` молчит на 403, убран assert из `_wait_company_absent`.

### Проверка удаления компании по ID
**Проблема:** `GET /companies/{id}` возвращал 200 ещё 60+ секунд после успешного DELETE.  
**Фикс:** `_gone` теперь проверяет `GET /companies` (список) вместо GET по ID, timeout=120s.

### Контакт: assert в finally + неверный endpoint
**Проблема:** `DELETE /subscriptions/{sub_id}/contacts` — это "убрать из подписки", не "удалить объект". `GET /accounts/contacts/{id}` после этого всё равно 200.  
**Фикс:** Проверяем только статус DELETE-ответа, не ждём "gone".

### Prod 401 на всех сервисах
**Проблема:** `config/config.py` имеет `HOST = get_host()` на уровне модуля — вычисляется при импорте до загрузки `.env.prod`.  
**Фикс:** `scripts/run_allure_local.sh` — добавлен `ENVIRON="$ENV_NAME"` перед вызовом pytest.

### Pydantic ValidationError на prod
- `CardByIdPersonModel` — добавлено `selfInfo: Optional[str]`
- `AccountContactByIdModel` — добавлено `cardID: Optional[int]`
- `ClientTokensGetAPI` — принимает 204 (нет зарегистрированного токена), возвращает пустую модель
- `PowerBIReportItemModel` — добавлены `isCommon`, `reportType`, `reportServiceUrl`

### Миграция сервисов на `self._call()`
**Задача:** 183 сервиса имели идентичный 5-строчный boilerplate (`start = time.time()` + `requests.METHOD()` + `attach_time` + `attach_url` + `attach_response`).  
**Фикс:** Добавлен `_call()` в `Helper`. Все 183 сервиса мигрированы автоматически (скриптом `migrate_to_call.py`, затем удалён). 9 сервисов с retry-логикой — вручную (внутри retry-цикла).  
**Эффект:** Любое изменение в логике HTTP-запросов достаточно сделать в одном месте — `src/support/helper.py`.

### Баг в `wait_until` (молчаливый falsy)
**Проблема:** `if last:` в `src/support/waiter.py` считал `0`, `False`, `[]`, `""` за "не готово".  
**Фикс:** Заменено на `if last is not None:`.

### Удалён `config/base_test.py`
**Проблема:** 300-строчный файл с инстанцированием 100+ API-классов в `setup_method` — никем не импортировался и не использовался.  
**Фикс:** Удалён.

### Raw requests убраны из тестов и хелперов
**Проблема:** В 7 файлах (`test_accounts_card_delete.py`, `test_accounts_card_catalog.py`, `tests/api/contacts/conftest.py`, `tests/e2e/contacts/helpers.py`, `tests/api/subscriptions/helpers.py`, `test_account_actions_smoke.py`, `test_mobile_account_verification_email_flow.py`) были прямые вызовы `requests.get/delete` в waiter-функциях и cleanup-блоках — вне Allure-контекста.  
**Фикс:** Все заменены на `_helper._call()`. В root `conftest.py::_get_api_user_access_token` — оставлен `requests.post` намеренно (auth bootstrap до старта тестов, вне Allure).

### Параметризованные негативные тесты авторизации
**Добавлено:** `tests/api/test_invalid_auth_parametrize.py` — 12 тестов: 4 критичных endpoint × 3 сценария плохого токена (`""`, `"garbage"`, `malformed JWT`). Все ожидают 401/403.  
**Паттерн:** `class TestInvalidAuthParametrize(Helper)` + `@pytest.mark.parametrize` по двум осям.

### Allure environment.properties
**Добавлено:** В отчёт Allure теперь пишутся `DATE` (дата запуска) и `PYTHON` (версия интерпретатора) вместе с `ENVIRONMENT`, `HOST`, `APP_ID`.

### `@allure.title` на всех тест-методах
**Проблема:** Часть тест-методов не имела `@allure.title` — в Allure-отчёте отображалось техническое имя `test_*`.  
**Фикс:** Добавлены аннотации во всех файлах, где они отсутствовали.

### Fixtures cleanup
**Проблема:** `testkit/fixtures/company.py` содержал `company_logo_color_ctx` и `company_simple_flow_ctx` — мёртвые фикстуры, не используемые ни одним тестом.  
**Фикс:** Файл удалён, убран из `pytest_plugins` в root `conftest.py`.  
**Проблема:** `leadgen_field_template_id` была определена дважды — в `tests/api/conftest.py` и `tests/e2e/cards/conftest.py`.  
**Фикс:** Объединена в root `conftest.py` с `scope="session"`.

### CardAttribute Delete (087/087.1) — известная проблема
**Проблема:** В ответе GET /attributes record id находится в `cardAttribute.id`, а не в `id`.  
**Статус:** Сервисы созданы, тесты удалены до прояснения формата DELETE body.

## Переписанные тесты (ctx → try/finally)

| Файл | Было | Стало |
|---|---|---|
| `tests/e2e/company/test_company_create_get_delete_flow.py` | fixture ctx | try/finally |
| `tests/e2e/company/test_company_create_and_edit_get_delete_flow.py` | fixture ctx | try/finally |
| `tests/e2e/company/test_company_create_withlogoandcolor_get_delete_flow.py` | fixture ctx | try/finally |
| `tests/api/accounts/test_accounts_contact_create_for_owner.py` | assert в finally | try/finally |
| `tests/e2e/contacts/test_contact_create_and_delete.py` | 4 метода + fixture | 1 метод try/finally |
| `tests/e2e/employee/test_employee_invitation_add_moveincompany_delete_flow.py` | 6 методов + fixture | 1 метод try/finally |
| `tests/e2e/employee/test_employee_invitation_add_copyincompany_delete_flow.py` | 6 методов + fixture | 1 метод try/finally |

## Новые сервисы (добавлены в текущей сессии)

### AccountTokens
| Сервис | Метод | Путь |
|---|---|---|
| `account_tokens/account_tokens_add` | POST | `/accounttokens/` |
| `account_tokens/account_tokens_get` | GET | `/accounttokens/{token}` |
| `account_tokens/account_tokens_delete` | DELETE | `/accounttokens/{token}` |

### Attributes (CRUD)
| Сервис | Метод | Путь |
|---|---|---|
| `attributes/attribute_create` | POST | `/Attributes` — body: `[{"attributeTypeID": N, "name": "..."}]` |
| `attributes/attribute_update` | PUT | `/Attributes` — body: `[{"id": N, "name": "..."}]` |
| `attributes/attribute_delete_by_id` | DELETE | `/Attributes/{id}` |
| `attributes/attribute_delete_many` | DELETE | `/Attributes` — body: `[id1, id2]` |

> Тесты для create/update/delete убраны (проблемы с AttributeTypeID). GET тесты работают.

### CardAttributes (085–087)
| Сервис | Метод | Путь |
|---|---|---|
| `cards/card_attributes_list` | GET | `/cards/{id}/attributes/` |
| `cards/card_link_attributes` | GET | `/cards/{token}/cardLink/attributes` |
| `accounts/accounts_card_attributes_list` | GET | `/accounts/{id}/cards/{cardId}/attributes/` |
| `cards/card_attributes_merge` | PUT | `/cards/{id}/attributes` |
| `accounts/accounts_card_attributes_merge` | PUT | `/accounts/{id}/cards/{cardId}/attributes` |
| `cards/card_attributes_delete` | DELETE | `/cards/{id}/attributes` — body: `[record_id]` |
| `accounts/accounts_card_attributes_delete` | DELETE | `/accounts/{id}/cards/{cardId}/attributes` — body: `[record_id]` |

> Payload для merge: `[{"AttributeID": N, "Name": "...", "SortOrder": 1, "Value": ["..."], "IsEnabled": true, "AttributeFormID": null}]`

### CardAttributeAttachments (083–084)
| Сервис | Метод | Путь |
|---|---|---|
| `cards/card_attribute_attachment_upload` | PUT | `/Cards/{id}/upload/fromForm` — multipart |
| `cards/card_attribute_attachments` | GET | `/cards/{id}/attributes/attachments` |
| `cards/card_link_attribute_attachments` | GET | `/cards/{token}/cardLink/attributes/attachments` |
| `accounts/accounts_card_attribute_attachments` | GET | `/accounts/{id}/cards/{cardId}/attributes/attachments` |

> **083 Upload:** метод PUT (не POST!). Форма: `AttributeID` (type ID), `CardAttributeID` (record ID из `cardAttribute.id`), `Attachments.Index=0`, `Attachments[0].File`, `Attachments[0].IsIgnorePossibleDuplication=true`.  
> Перед загрузкой нужен merge атрибута, затем GET attributes для получения `cardAttribute.id`.

### Locations (096.1.1, 096.2.1)
| Сервис | Метод | Путь |
|---|---|---|
| `locations/location_cardlink_by_id` | GET | `/cards/attributes/locations/{id}/cardlink/{token}` |
| `locations/location_cardlinks_list` | GET | `/cards/attributes/locations/cardlink/{token}` |

### CardLinks
| Сервис | Метод | Путь |
|---|---|---|
| `cardlinks/cardlink_catalog_by_id` | GET | `/cardlinks/{token}/catalog/{id}` — ожидается 204 |
| `cards/card_link_leadgen_form_by_id` | GET | `/cards/{token}/cardLink/leadGenForms/{formId}` |

### PowerBI (805, 806)
| Сервис | Метод | Путь |
|---|---|---|
| `powerbi_reports/powerbi_reports_list` | GET | `/powerbireports/` |
| `powerbi_reports/powerbi_report_by_id` | GET | `/powerbireports/{id}` |

### Proxy (901)
| Сервис | Метод | Путь |
|---|---|---|
| `proxy/proxy_card_cardlink` | GET | `/proxy/card/cardlink/{token}` |

### Subscriptions (604, 604.1)
| Сервис | Метод | Путь |
|---|---|---|
| `subscriptions/subscription_request` | POST | `/Subscriptions/request` — **публичный, без авторизации** |
| `subscriptions/subscription_contacts_list` | GET | `/Subscriptions/{id}/contacts?accountID=` |

> **604 Subscription/Request:** публичный endpoint (без auth). Body PascalCase: `Email`, `CompanyName`, `FirstName`, `LastName`, `MobilePhone`, `Position`, `InvitationsLimit`. Email — рандомный через `uuid`. `SupportCardLinkID` — необязателен.  
> **604.1 Subscription/ContactList:** обязателен query param `?accountID=`. Ответ — массив: `accountID`, `cardID`, `contactID`, `firstName`, `lastName`, `mobilePhone`, `position`, `created`.

### Известные особенности поведения

| Ручка | Особенность |
|---|---|
| `GET /cardlinks/{token}/catalog/{id}` | Без auth с фейковым токеном → 409 CardLinkInvalid (токен валидируется до проверки auth) |
| `GET /Subscriptions/{id}/contacts` | Требует `?accountID=` иначе 409 |
| `POST /Subscriptions/request` | Публичный endpoint, не требует JWT |
| `PUT /cards/{token}/cardLink/attributes/click` | Body: `{"AttributeID": <type_id>, "CardAttributeID": <sort_order>}`. Оба поля обязательны. `CardAttributeID` = SortOrder атрибута (обычно 1) |
| `POST /accounttokens/` | Body не нужен вообще |
| `CardAttribute.id` | В ответе GET всегда `null`; реальный record ID — в `cardAttribute.id` (вложенный объект) |
| `PATCH /accounts/{id}/cards/{id}` (v1) | Поддерживает только `[{"Field": "CompanyID", "Value": N}]`. `FirstName` и другие поля → 409 ParameterOutOfRange. Для других полей использовать v2/v3 |
| `GET /accounts/{id}/cards/{id}/links/{cardLink}` | Поведение на dev не соответствует контракту — тест намеренно не написан |
| `GET /Cards/{id}/customMessageTemplates` (cards-scope) | Возвращает 404 на dev — legacy endpoint, не функционирует. Использовать accounts-scope `/Accounts/{id}/CustomMessageTemplates` |
| `GET /VirtualBackgrounds` (add/remove flow) | На dev нет виртуальных фонов → flow-тесты пропускаются через `pytest.skip`. На prod работают |
| AccountActions 011/013/014 | Ответ может быть list (не dict) → защита `if isinstance(data, list): data = {"errors": data}` во всех трёх сервисах |

## Покрытие по Postman (статус)

### Не покрыто тестами (сервисы есть, тестов нет)
- `598` Subscription/List — `GET /Subscriptions` (возвращает 404 на dev, возможно admin-only)
- `599` Subscription/Get — `GET /Subscriptions/{id}/account/{accountId}` (возвращает 404 на dev)

### Намеренно пропущено
- `010` AccountVerification — `[OBSOLETE]`
- `096.3–5` Location Add/Update/Delete — нет контроля над данными, нельзя создавать/удалять в тестах
- `500/510` AccountActions Purge/Delete — деструктивные admin операции
- `600/601` Subscription/Notification — webhook, трудно тестировать
- `802/802.1` AppleWallet — мобильная специфика
- `804` Imports/xlsx — сложный file import
- `GET /Cards/{id}/customMessageTemplates` — legacy, 404 на dev (покрыто через accounts-scope)

## Полезные команды

```bash
# Запуск всех тестов
pytest --env=dev -v

# Только smoke
pytest --env=dev -m smoke -v

# Конкретный файл
pytest tests/e2e/company/test_company_create_get_delete_flow.py -v

# На prod (ENVIRON обязателен перед pytest)
ENVIRON=prod pytest --env=prod -v

# С allure
pytest --env=dev --alluredir=allure-results
allure generate allure-results -o allure-report --clean
allure open allure-report
```

## Важные endpoints

```
POST   /companies                                         — создать компанию
GET    /companies                                         — список компаний (для проверки удаления)
GET    /companies/{id}                                    — компания по id
PUT    /companies/{id}                                    — обновить компанию
DELETE /companies/{id}                                    — удалить компанию
PUT    /companies/{id}/designsettings                     — цвет и фон
GET    /companies/{id}/designsettings                     — проверить цвет и фон
POST   /attachments                                       — загрузить файл
POST   /Subscriptions/{sub_id}/invitation                 — создать сотрудника
DELETE /Subscriptions/{sub_id}/invitation/{id}            — удалить сотрудника
DELETE /subscriptions/{sub_id}/contacts                   — убрать контакт из подписки
POST   /accounttokens/                                    — создать токен (без body)
GET    /accounttokens/{token}                             — получить токен
DELETE /accounttokens/{token}                             — удалить токен
GET    /powerbireports/                                   — список PowerBI отчётов
GET    /powerbireports/{id}                               — отчёт по id
GET    /proxy/card/cardlink/{token}                       — proxy cardlink
GET    /cards/{id}/attributes/                            — атрибуты карточки
PUT    /cards/{id}/attributes                             — merge атрибутов
DELETE /cards/{id}/attributes                             — удалить атрибуты (body: [record_id])
GET    /cards/{id}/attributes/attachments                 — вложения атрибутов
PUT    /Cards/{id}/upload/fromForm                        — загрузить файл к атрибуту (multipart)
GET    /Subscriptions/{id}/contacts?accountID=            — контакты подписки
POST   /Subscriptions/request                             — запрос на подписку (публичный, без auth)
```

## Замечания

- `.tmp_postman_items_new.txt` — список ручек из Postman, для справки, не удалять
- `.env.dev` и `.env.prod` содержат токены — в git не коммитить (прописаны в .gitignore)
- Количество тестов: ~385+ (api: ~130 файлов, e2e: ~40 файлов)
- Модели с `extra="allow"` (`BaseModel`) — для нестабильных/публичных ответов (cardAttributes, cardlinks)
- Модели с `extra="forbid"` (`StrictBaseModel`) — для стабильных LK ответов
- Запуск тестов: `ENVIRON=dev .venv/Scripts/pytest tests/ -v` (venv активировать через `.venv/Scripts/pytest` напрямую)
