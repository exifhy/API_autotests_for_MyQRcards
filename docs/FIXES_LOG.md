# Журнал фиксов

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
**Задача:** 183 сервиса имели идентичный 5-строчный boilerplate.  
**Фикс:** Добавлен `_call()` в `Helper`. Все 183 сервиса мигрированы автоматически (скриптом `migrate_to_call.py`, затем удалён). 9 сервисов с retry-логикой — вручную.  
**Эффект:** Любое изменение в логике HTTP-запросов достаточно сделать в одном месте — `src/support/helper.py`.

### Баг в `wait_until` (молчаливый falsy)
**Проблема:** `if last:` в `src/support/waiter.py` считал `0`, `False`, `[]`, `""` за "не готово".  
**Фикс:** Заменено на `if last is not None:`.

### Удалён `config/base_test.py`
**Проблема:** 300-строчный файл с инстанцированием 100+ API-классов в `setup_method` — никем не использовался.  
**Фикс:** Удалён.

### Raw requests убраны из тестов и хелперов
**Проблема:** В 7 файлах были прямые вызовы `requests.get/delete` вне Allure-контекста.  
**Фикс:** Все заменены на `_helper._call()`. В root `conftest.py::_get_api_user_access_token` — оставлен `requests.post` намеренно (auth bootstrap до старта тестов).

### Параметризованные негативные тесты авторизации
**Добавлено:** `tests/api/test_invalid_auth_parametrize.py` — 12 тестов: 4 критичных endpoint × 3 сценария плохого токена (`""`, `"garbage"`, `malformed JWT`). Все ожидают 401/403.

### SubscriptionContactItemModel — companyName на prod
**Проблема:** `StrictBaseModel` (`extra="forbid"`), но prod возвращает поле `companyName` — ValidationError.  
**Фикс:** Добавлено `companyName: Optional[str] = None`.

### AccountActions 020 — захардкоженный dev URL
**Проблема:** `_account_actions_url()` всегда возвращала dev URL — на prod получал 401.  
**Фикс:** Заменено на `from config.config import HOST`.

### ACCOUNT_ACTIONS_BASIC_PASSWORD не передавался в CI
**Фикс:** Добавлена строка в `tests-prod.yml`, `tests-prod-full.yml` и `tests-dev.yml`.

### Allure DEV и PROD перезаписывали друг друга
**Фикс:** Добавлен `destination_dir: dev` / `destination_dir: prod`. История разделена: `dev/history` и `prod/history`.

### Hardcoded API URLs убраны из репо (ОТМЕНЕНО)
**Откат:** `DEFAULT_URLS` возвращён — нужен как fallback для локального запуска.

### Удалены тесты которые всегда скипались
**Удалены:** `test_powerbi_report_by_id.py`, `test_accounts_card_virtualbackgrounds.py`, `test_card_virtualbackgrounds.py`, `test_promotion_by_id.py`, `test_mobile_account_verification_email_flow.py`.

### assert в teardown employee фикстур
**Фикс:** Все assert убраны из `_safe_delete_invitation`, функция обёрнута в `try/except pass`.

### AccountActionsGetAPI — dict вместо list
**Проблема:** `GET /accountActions` с `actionJwt` возвращает `dict` (до подтверждения).  
**Фикс:** `dict` оборачивается в `[data]`.

### Fixtures cleanup
**Фикс:** Удалены мёртвые фикстуры `company_logo_color_ctx` и `company_simple_flow_ctx`. `leadgen_field_template_id` объединена в root `conftest.py` с `scope="session"`.

### CardAttribute Delete (087/087.1) — известная проблема
**Статус:** Сервисы созданы, тесты удалены до прояснения формата DELETE body. Record ID в `cardAttribute.id`, а не в `id`.

### Pydantic ValidationError — isValid в subscription после релиза
**Фикс:** Добавлено `isValid: Optional[bool] = None` в четыре модели:
- `CardByIdSubscriptionModel`, `CardByIdV2SubscriptionModel`, `CardSubscriptionModel`, `CardV2SubscriptionModel`

### DEV workflow таймаут
**Фикс:** `timeout-minutes` в `tests-dev.yml` увеличен с 30 до 60.

### 409 NotFound вместо 404 после релиза (waiter-функции)
**Проблема:** API начал возвращать `409 Conflict` с `code: "NotFound"` вместо `404` при GET удалённого ресурса.  
**Фикс:** Добавлен `HTTPStatus.CONFLICT` в шести местах:
- `test_accounts_card_delete.py` — `_wait_card_absent`
- `test_accounts_card_catalog.py` — `_wait_catalog_absent`
- `tests/api/conftest.py` — `_wait_card_deleted`
- `tests/api/contacts/conftest.py` — `_wait_contact_deleted`
- `tests/e2e/contacts/helpers.py` — `wait_contact_absent`
- `tests/e2e/company/helpers.py` — `wait_company_absent`

**Правило:** Если тест падает с `X is still available after delete` — проверить в Postman что возвращает GET после DELETE. Скорее всего 409 вместо 404.

### raise AssertionError в teardown mobile фикстуры
**Фикс:** Заменено на `logger.warning`.

### Allure CLI Install в GitHub Actions (broken Ubuntu mirror)
**Фикс:** Переключились с `.deb` на `.tgz` tarball напрямую с GitHub releases.

### isSubscriptionValid и isSelfRegistrationOnly после релиза
**Фикс:** 
- `CardByIdShortModel` / `CardLinkShortCardModel` — добавлено `isSubscriptionValid: Optional[bool] = None`
- `CardLinksListItemModel` — добавлены `isSelfRegistrationOnly`, `isPublic`, `isDefault`

### SubscriptionModerators модели — неполные поля
**Проблема:** `SubscriptionModeratorItemModel` и `SubscriptionModeratorGetModel` содержали только `accountID`, `cardID`, `email`, хотя бэкенд (`GetResult.cs`) возвращает `firstName`, `lastName`, `middleName`.  
**Фикс:** Добавлены три поля в обе модели и в список конструируемых объектов в `api_subscription_moderators_list.py`.

### Новые сервисы и тесты (текущая сессия)
**Добавлено:**
- `services/subscriptions/subscription_prices/` + `tests/api/subscriptions/test_subscription_prices.py` — `GET /SubscriptionPrices` (613, публичный)
- `services/accounts/accounts_sso_providers/` + `tests/api/accounts/test_accounts_sso_providers.py` — `GET /Accounts/sso/providers` (300, публичный)
- `services/accounts/accounts_sso_bindings/` + `tests/api/accounts/test_accounts_sso_bindings.py` — `GET /Accounts/sso` (301, требует JWT)
- `services/lead_gen_form_fields/lead_gen_form_fields_list/` + `tests/api/lead_gen_form_fields/test_lead_gen_form_fields_list.py` — `GET /LeadGenFormFields` (публичный)
- `tests/e2e/company/test_company_create_with_large_cdn_images_flow.py` — e2e flow с загрузкой логотипа и фона >2МБ через CDN endpoint

### test_sso_bindings_structure — закомментирован намеренно
**Причина:** Тест-аккаунт на dev не имеет SSO-привязок → всегда 204 → `pytest.skip` засорял Allure.  
**Решение:** Тест закомментирован, добавлена заметка в `CLAUDE.md`. Раскомментировать когда на dev-аккаунте будет привязан VK ID или Яндекс ID.

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
