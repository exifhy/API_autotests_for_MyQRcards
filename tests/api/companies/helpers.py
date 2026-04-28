import requests

from services.accounts.accounts_list.api_accounts_list import AccountsListAPI
from services.companies.company_by_id.api_company_by_id import CompanyByIdAPI
from services.companies.company_designsettings_by_id.api_company_designsettings_by_id import (
    CompanyDesignsettingsByIdAPI,
)
from src.support.waiter import wait_until


def wait_company_by_id(company_id: int, *, timeout_s: int = 60, step_s: int = 3):
    def _get_company():
        try:
            return CompanyByIdAPI().get_company_by_id(company_id)
        except AssertionError:
            return None

    return wait_until(_get_company, timeout_s=timeout_s, step_s=step_s)


def wait_company_deleted(company_id: int, *, timeout_s: int = 60, step_s: int = 3):
    def _deleted():
        try:
            CompanyByIdAPI().get_company_by_id(company_id)
            return None
        except AssertionError:
            return True

    return wait_until(_deleted, timeout_s=timeout_s, step_s=step_s)


def wait_company_matches(company_id: int, expected: dict, *, timeout_s: int = 60, step_s: int = 3):
    def _get_updated_company():
        model = wait_company_by_id(company_id, timeout_s=1, step_s=step_s)
        if model is None:
            return None

        checks = (
            ("name", "Name"),
            ("email", "Email"),
            ("phone", "Phone"),
            ("activity", "Activity"),
            ("customers", "Customers"),
        )
        for model_field, payload_field in checks:
            if payload_field in expected and getattr(model, model_field, None) != expected[payload_field]:
                return None
        return model

    return wait_until(_get_updated_company, timeout_s=timeout_s, step_s=step_s)


def wait_company_designsettings_by_id(company_id: int, *, timeout_s: int = 60, step_s: int = 3):
    def _get_designsettings():
        try:
            return CompanyDesignsettingsByIdAPI().get_company_designsettings(company_id)
        except AssertionError:
            return None

    return wait_until(_get_designsettings, timeout_s=timeout_s, step_s=step_s)


def wait_account_present_in_company(
    account_id: int,
    company_id: int,
    *,
    include_subscription_owner: bool = True,
    timeout_s: int = 90,
    step_s: int = 5,
):
    def _present():
        try:
            _, accounts = AccountsListAPI().get_accounts(
                company_id=company_id,
                include_subscription_owner=include_subscription_owner,
            )
        except requests.RequestException:
            return None
        return True if any(item.id == account_id for item in accounts.items) else None

    return wait_until(_present, timeout_s=timeout_s, step_s=step_s)


def assert_company_matches_payload(model, payload: dict, *, company_id: int) -> None:
    assert model.id == company_id
    assert model.name == payload["Name"]
    assert model.email == payload["Email"]
    assert model.phone == payload["Phone"]
    assert model.activity == payload["Activity"]
    if "Customers" in payload:
        assert model.customers == payload["Customers"]


def assert_company_designsettings_match(model, payload: dict, *, company_id: int) -> None:
    assert model.companyID == company_id
    assert model.color == payload["Color"]
    assert model.qrColor == payload["QRColor"]
    assert model.backgroundAttachmentID in (None, payload["BackgroundAttachmentID"])


def assert_companies_list_model(model) -> None:
    assert isinstance(model.items, list)
    assert model.items, "Companies list is empty"
    assert model.items[0].id is not None
    assert model.items[0].name is None or model.items[0].name != ""
