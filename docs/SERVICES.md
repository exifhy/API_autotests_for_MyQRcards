# Сервисы и API — справочник

## Новые сервисы

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

### Attachments CDN (081.1)
| Сервис | Метод | Путь |
|---|---|---|
| `attachments/attachment_upload_cdn` | POST | `{UPLOAD_HOST}/attachments/v2/` |

> **CDN upload:** multipart form-data. Поля: `Attachments.Index=0`, `Attachments[0].File`, `Attachments[0].IsIgnorePossibleDuplication=true`. Лимит 100МБ.  
> Ответ: `{"attachments": [{"id": N, "url": "https://api.selcdn.ru/...", "fileName": "..."}]}`  
> `UPLOAD_HOST` = `dev-upload.myqrcards.com` (dev) / `upload.myqrcards.com` (prod)

### Subscriptions (604, 604.1, 613)
| Сервис | Метод | Путь |
|---|---|---|
| `subscriptions/subscription_request` | POST | `/Subscriptions/request` — **публичный, без авторизации** |
| `subscriptions/subscription_contacts_list` | GET | `/Subscriptions/{id}/contacts?accountID=` |
| `subscriptions/subscription_prices` | GET | `/SubscriptionPrices` — **публичный, без авторизации** |

> **604:** Body PascalCase: `Email`, `CompanyName`, `FirstName`, `LastName`, `MobilePhone`, `Position`, `InvitationsLimit`.  
> **604.1:** Обязателен query param `?accountID=`.  
> **613:** Возвращает список тарифных планов. Публичный endpoint, не требует JWT.

### AccountActions Silent (011.2, 012.2, TASK 30718)
| Сервис | Метод | Путь |
|---|---|---|
| `account_actions_mobile_account_verification` | POST | `/accountActions/MobileAccountVerification/silent` |
| `account_actions_web_account_verification` | POST | `/accountActions/WebAccountVerification/silent` |

> Аналогичны 011/012, но без отправки email. Auth: Basic (`ACCOUNT_ACTIONS_BASIC_PASSWORD`). Body: `{"email": "..."}`. Ожидается 202 + `actionJwt` + `actionToken`.

### SSO (300, 301)
| Сервис | Метод | Путь |
|---|---|---|
| `accounts/accounts_sso_providers` | GET | `/Accounts/sso/providers` — **публичный, без авторизации** |
| `accounts/accounts_sso_bindings` | GET | `/Accounts/sso` — требует авторизации |

> **300 `/Accounts/sso/providers`:** Справочник доступных SSO-провайдеров (VK, Яндекс и др.). Публичный endpoint. Модель: `SsoProviderModel` (`providerType`, `code`, `nameRu`, `nameEn`).  
> **301 `/Accounts/sso`:** Список SSO-привязок текущего аккаунта. Возвращает 200 со списком или 204 если привязок нет. `test_sso_bindings_structure` закомментирован — тест-аккаунт не имеет SSO-привязок.

### LeadGenFormFields
| Сервис | Метод | Путь |
|---|---|---|
| `lead_gen_form_fields/lead_gen_form_fields_list` | GET | `/LeadGenFormFields` — **публичный, без авторизации** |

> Справочник полей лид-формы. Публичный endpoint. Модель: `LeadGenFormFieldModel` (`id`, `name`, `nameRu`, `nameEn`).

## Известные особенности поведения

| Ручка | Особенность |
|---|---|
| `GET /cardlinks/{token}/catalog/{id}` | Без auth с фейковым токеном → 409 CardLinkInvalid (токен валидируется до проверки auth) |
| `GET /Subscriptions/{id}/contacts` | Требует `?accountID=` иначе 409 |
| `POST /Subscriptions/request` | Публичный endpoint, не требует JWT |
| `PUT /cards/{token}/cardLink/attributes/click` | Body: `{"AttributeID": <type_id>, "CardAttributeID": <sort_order>}`. `CardAttributeID` = SortOrder (обычно 1) |
| `POST /accounttokens/` | Body не нужен вообще |
| `CardAttribute.id` | В ответе GET всегда `null`; реальный record ID — в `cardAttribute.id` (вложенный объект) |
| `PATCH /accounts/{id}/cards/{id}` (v1) | Поддерживает только `CompanyID`. Для других полей использовать v2/v3 |
| `GET /accounts/{id}/cards/{id}/links/{cardLink}` | Поведение на dev не соответствует контракту — тест намеренно не написан |
| `GET /Cards/{id}/customMessageTemplates` (cards-scope) | 404 на dev — legacy. Использовать `/Accounts/{id}/CustomMessageTemplates` |
| `GET /VirtualBackgrounds` | На dev данных нет → pytest.skip. На prod работает |
| AccountActions 011/013/014 | Ответ может быть list → `if isinstance(data, list): data = {"errors": data}` |
| `GET /accounts/{id}/cards/links` (049) | После релиза возвращает `isSelfRegistrationOnly` — поле добавлено в `CardLinksListItemModel` |
| `GET /cards/{id}/V2?AllData=true` | С флагом возвращает 200 вместо 409 для карточек с истёкшей подпиской. `subscription.isValid=False`. Нужен `EXPIRED_JWT`. |
| `GET /cardLinks/{token}/card?AllData=true` | Публичный. Возвращает 200 + данные карточки с истёкшей подпиской. |
| `GET /cardLinks/{token}/short/card?AllData=true` | Публичный. Возвращает 200 + `isSubscriptionValid=False`. |

## Покрытие по Postman (статус)

### Не покрыто тестами (сервисы есть, тестов нет)
- `598` Subscription/List — `GET /Subscriptions` (возвращает 404 на dev, возможно admin-only)
- `599` Subscription/Get — `GET /Subscriptions/{id}/account/{accountId}` (возвращает 404 на dev)

### Намеренно пропущено
- `010` AccountVerification — `[OBSOLETE]`
- `096.3–5` Location Add/Update/Delete — нет контроля над данными
- `500/510` AccountActions Purge/Delete — деструктивные admin операции
- `600/601` Subscription/Notification — webhook, трудно тестировать
- `802/802.1` AppleWallet — мобильная специфика
- `804` Imports/xlsx — сложный file import
- `GET /Cards/{id}/customMessageTemplates` — legacy, 404 на dev

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
GET    /proxy/card/cardlink/{token}                       — proxy cardlink
GET    /cards/{id}/attributes/                            — атрибуты карточки
PUT    /cards/{id}/attributes                             — merge атрибутов
DELETE /cards/{id}/attributes                             — удалить атрибуты (body: [record_id])
GET    /cards/{id}/attributes/attachments                 — вложения атрибутов
PUT    /Cards/{id}/upload/fromForm                        — загрузить файл к атрибуту (multipart)
GET    /Subscriptions/{id}/contacts?accountID=            — контакты подписки
POST   /Subscriptions/request                             — запрос на подписку (публичный, без auth)
GET    /SubscriptionPrices                                — список тарифов (публичный, без auth)
GET    /Accounts/sso/providers                            — справочник SSO-провайдеров (публичный, без auth)
GET    /Accounts/sso                                      — SSO-привязки текущего аккаунта (требует JWT)
GET    /LeadGenFormFields                                 — поля лид-формы (публичный, без auth)
POST   {UPLOAD_HOST}/attachments/v2/                      — CDN upload (лимит 100МБ)
```
