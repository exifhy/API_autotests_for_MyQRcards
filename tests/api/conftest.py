import time
from http import HTTPStatus

import pytest

from config.config import get_host
from config.headers import Headers
from src.support.helper import Helper
from src.support.token_utils import get_token
from src.support.waiter import wait_until

_helper = Helper()


def _api_host() -> str:
    return get_host().rstrip("/")


def _wait_card_deleted(card_id: int, *, timeout_s: int = 60, step_s: int = 3) -> bool:
    url = f"{_api_host()}/Cards/{int(card_id)}"

    def _gone():
        response = _helper._call(
            "GET",
            url=url,
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        if response.status_code in (HTTPStatus.NO_CONTENT, HTTPStatus.NOT_FOUND):
            return True
        return None

    return bool(wait_until(_gone, timeout_s=timeout_s, step_s=step_s))


def _delete_card_best_effort(card_id: int) -> None:
    url = f"{_api_host()}/Cards/{int(card_id)}"
    last_error = None
    for _ in range(3):
        try:
            response = _helper._call(
                "DELETE",
                url=url,
                headers=Headers.auth_header(bearer_token=get_token()),
            )
            if response.status_code in (HTTPStatus.ACCEPTED, HTTPStatus.NOT_FOUND):
                if response.status_code == HTTPStatus.NOT_FOUND or _wait_card_deleted(card_id):
                    return
                last_error = AssertionError(f"Card {card_id} is still returned by GET after delete")
                continue
            last_error = AssertionError(
                f"Unexpected DELETE status for card {card_id}: {response.status_code} {response.text}"
            )
        except Exception as error:
            last_error = error
        time.sleep(1)

    if last_error is not None:
        raise last_error


@pytest.fixture(autouse=True)
def cleanup_created_cards(monkeypatch):
    from services.cards.card_create.api_card_create import CardCreateAPI
    from services.cards.card_create_v2.api_card_create_v2 import CardCreateV2API

    created_card_ids: list[int] = []
    original_create_card = CardCreateAPI.create_card
    original_create_card_v2 = CardCreateV2API.create_card_v2

    def _wrapped_create_card(self, *args, **kwargs):
        model = original_create_card(self, *args, **kwargs)
        card_id = getattr(model, "id", None)
        if isinstance(card_id, int):
            created_card_ids.append(card_id)
        return model

    def _wrapped_create_card_v2(self, *args, **kwargs):
        model = original_create_card_v2(self, *args, **kwargs)
        card_id = getattr(model, "id", None)
        if isinstance(card_id, int):
            created_card_ids.append(card_id)
        return model

    monkeypatch.setattr(CardCreateAPI, "create_card", _wrapped_create_card)
    monkeypatch.setattr(CardCreateV2API, "create_card_v2", _wrapped_create_card_v2)

    yield

    seen: set[int] = set()
    for card_id in reversed(created_card_ids):
        if card_id in seen:
            continue
        seen.add(card_id)
        try:
            _delete_card_best_effort(card_id)
        except Exception:
            pass


@pytest.fixture
def created_card(cfg):
    from services.cards.card_by_id.api_card_by_id import CardByIdAPI
    from services.cards.card_create.api_card_create import CardCreateAPI

    model = CardCreateAPI().create_card(
        subscription_id=cfg["subscription_id"],
        company_id=cfg["company_id_create"],
    )
    assert model.id is not None

    def _card_available():
        try:
            return CardByIdAPI().get_card_by_id(model.id)
        except AssertionError:
            return None

    available_card = wait_until(_card_available, timeout_s=30, step_s=2)
    assert available_card is not None, f"Created card {model.id} did not become available in time"
    return model


@pytest.fixture
def created_company():
    from services.companies.company_create.api_company_create import CompanyCreateAPI
    from services.companies.company_create.payloads import Payloads
    from services.companies.company_delete_by_id.api_company_delete_by_id import (
        CompanyDeleteByIdAPI,
    )
    from tests.api.companies.helpers import wait_company_deleted

    payload = Payloads.build_company_create_payload()
    _, create_model = CompanyCreateAPI().create_company(payload)
    company_id = int(create_model.id)
    ctx = {
        "id": company_id,
        "payload": payload,
    }

    try:
        yield ctx
    finally:
        try:
            response = CompanyDeleteByIdAPI().delete_company_by_id(company_id)
            if response.status_code not in (HTTPStatus.FORBIDDEN, HTTPStatus.NOT_FOUND):
                wait_company_deleted(company_id, timeout_s=60, step_s=3)
        except Exception:
            pass
