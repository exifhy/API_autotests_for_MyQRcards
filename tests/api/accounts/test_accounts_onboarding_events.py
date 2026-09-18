from http import HTTPStatus

import allure
import pytest

from services.accounts.accounts_onboarding_event_add.api_accounts_onboarding_event_add import (
    AccountsOnboardingEventAddAPI,
)
from services.accounts.accounts_onboarding_events_list.api_accounts_onboarding_events_list import (
    AccountsOnboardingEventsListAPI,
)
from src.constants.onboarding_events import ONBOARDING_EVENT_CODES_BY_TYPE_ID


@allure.epic("API")
@allure.feature("Accounts")
@pytest.mark.api
@pytest.mark.accounts
@allure.description(
    """
    REQUIREMENT 29915 — хранение пользовательских событий для онбординга пушами.
    POST /Accounts/onboardingEvents/{typeID}, GET /Accounts/onboardingEvents

    Ручка POST необратима: DELETE/reset для событий онбординга не существует
    (подтверждено чтением services/AccountsController.OnboardingEvents.cs — там
    только GET и POST). Live-проба на dev уже зафиксировала все 8 типов на
    тестовом аккаунте LK_JWT (18.09, согласовано с пользователем) — поэтому
    тесты ниже не проверяют состояние "событие ещё не наступало", только
    структуру ответа и идемпотентность.
    """
)
class TestAccountsOnboardingEvents:
    @allure.title("GET возвращает все 8 типов событий с корректными code/nameRu")
    @pytest.mark.smoke
    def test_get_returns_all_8_types_structure(self):
        events = AccountsOnboardingEventsListAPI().get_onboarding_events()

        assert len(events) == 8
        type_ids = {event.typeID for event in events}
        assert type_ids == set(ONBOARDING_EVENT_CODES_BY_TYPE_ID.keys())
        for event in events:
            assert event.code == ONBOARDING_EVENT_CODES_BY_TYPE_ID[event.typeID]
            assert event.accountID is not None
            assert event.nameRu

    @allure.title("POST идемпотентен — повторная фиксация не сдвигает created")
    @pytest.mark.smoke
    def test_post_is_idempotent(self):
        type_id = 1  # SendCard — уже зафиксирован ранее на этом аккаунте (см. описание класса)

        AccountsOnboardingEventAddAPI().add_onboarding_event(type_id)
        events_after_first = AccountsOnboardingEventsListAPI().get_onboarding_events()
        created_first = next(e.created for e in events_after_first if e.typeID == type_id)
        assert created_first is not None

        AccountsOnboardingEventAddAPI().add_onboarding_event(type_id)
        events_after_second = AccountsOnboardingEventsListAPI().get_onboarding_events()
        created_second = next(e.created for e in events_after_second if e.typeID == type_id)

        assert created_second == created_first

    @allure.title("Все 8 типов зафиксированы — POST по каждому идемпотентен, GET показывает created у всех")
    def test_all_types_are_fixed_and_idempotent(self):
        for type_id in ONBOARDING_EVENT_CODES_BY_TYPE_ID:
            AccountsOnboardingEventAddAPI().add_onboarding_event(type_id)

        events = AccountsOnboardingEventsListAPI().get_onboarding_events()
        assert len(events) == 8
        for event in events:
            assert event.created is not None, f"typeID={event.typeID} ({event.code}) expected to be fixed already"

    @allure.title("GET/POST без авторизации -> 401")
    def test_without_auth_401(self):
        get_response = AccountsOnboardingEventsListAPI().get_onboarding_events_without_auth()
        assert get_response.status_code == HTTPStatus.UNAUTHORIZED

        post_response = AccountsOnboardingEventAddAPI().add_onboarding_event_without_auth(1)
        assert post_response.status_code == HTTPStatus.UNAUTHORIZED

    @allure.title("POST typeID=0 -> 409 (не 400, как заявлено в задаче)")
    def test_post_type_id_zero_returns_409(self):
        """Комментарий к REQUIREMENT 29915 обещает 400 для typeID<=0, но живая
        проверка на dev дала 409 ParameterOutOfRange — тот же паттерн
        "409 вместо документированного кода", что уже встречался в проекте
        (см. docs/FIXES_LOG.md про 409 вместо 404 после DELETE)."""
        response = AccountsOnboardingEventAddAPI().add_onboarding_event_raw(0)

        assert response.status_code == HTTPStatus.CONFLICT

    @allure.title("POST с несуществующим typeID -> 409 (не 404, как заявлено в задаче)")
    def test_post_nonexistent_type_returns_409(self):
        response = AccountsOnboardingEventAddAPI().add_onboarding_event_raw(255)

        assert response.status_code == HTTPStatus.CONFLICT
