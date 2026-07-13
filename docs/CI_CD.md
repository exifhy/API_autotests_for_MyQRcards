# CI/CD — GitHub Actions + Telegram + Allure

## Репозиторий
- **GitHub:** `https://github.com/exifhy/API_autotests_for_MyQRcards` (публичный)

## Расписание прогонов

| Время | Окружение | Scope | Workflow |
|---|---|---|---|
| 10:00 пн-пт (Moscow) | DEV | все тесты | `tests-dev.yml` |
| 02:00 каждую ночь (Moscow) | PROD | только smoke | `tests-prod.yml` |
| 23:00 воскресенье (Moscow) | PROD | все тесты | `tests-prod-full.yml` |

## Allure отчёты (GitHub Pages)
- DEV: `https://exifhy.github.io/API_autotests_for_MyQRcards/dev/`
- PROD: `https://exifhy.github.io/API_autotests_for_MyQRcards/prod/`

Каждое окружение деплоит в свою поддиректорию — не перезаписывают друг друга.  
История: `dev/history` и `prod/history` в ветке `gh-pages`.

## Workflow файлы
- `.github/workflows/tests-dev.yml` — DEV (все тесты, пн-пт), timeout 60 мин
- `.github/workflows/tests-prod.yml` — PROD smoke (ежедневно)
- `.github/workflows/tests-prod-full.yml` — PROD full (воскресенье)
- `scripts/notify_telegram.py` — уведомления в Telegram

## Azure DevOps Pipeline
- Файл: `azure-pipelines.yml` (в корне репо, только в Azure)
- Trigger: ручной (`trigger: none`)
- Pool: `ubuntu-latest`, Python 3.13
- Variable group: `myqrcards-secrets` (содержит `LK_JWT`, `APP_ID`, `ACCOUNT_ACTIONS_BASIC_PASSWORD`, `IDS_DEV_JSON`)
- Запускает тесты на DEV окружении
- Генерирует Allure отчёт и публикует как артефакт сборки (`allure-report`)

## GitHub Secrets (обязательные)

| Секрет | Описание |
|---|---|
| `LK_JWT` | JWT токен для dev |
| `LK_JWT_PROD` | JWT токен для prod |
| `APP_ID` | X-APPLICATION-ID (одинаковый для dev/prod) |
| `ACCOUNT_ACTIONS_BASIC_PASSWORD` | Basic-пароль для AccountActions (012/020) — нужен в dev и prod |
| `IDS_DEV_JSON` | содержимое `data/ids.dev.json` (обновлять при добавлении новых полей в ids.dev.json) |
| `IDS_PROD_JSON` | содержимое `data/ids.prod.json` (обновлять при добавлении новых полей в ids.prod.json) |
| `EXPIRED_JWT` | JWT аккаунта с истёкшей подпиской (для тестов AllData=true) |
| `TELEGRAM_BOT_TOKEN` | токен Telegram бота |
| `TELEGRAM_CHAT_ID` | ID чата для уведомлений |

## Ручной запуск
GitHub → Actions → Tests DEV / Tests PROD / Tests PROD Full → Run workflow

## Allure история
- `gh-pages` ветка создаётся автоматически после первого прогона
- GitHub Pages: Settings → Pages → Branch: `gh-pages` → `/ (root)`
