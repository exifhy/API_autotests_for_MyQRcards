import allure
import pytest
from http import HTTPStatus

from src.api.endpoints import EMPLOYEE_INVITATION_CREATE_PATH, EMPLOYEE_INVITATION_DELETE_PATH
from src.resources.api import accounts_list
from src.resources.helpers import find_account_in_list
from src.resources.uploads import upload_generated_image
from src.support.waiter import wait_until
from src.utils.randoms import rand_email, rand_phone_ru8, rand_word


def _safe_delete_invitation(lk_api, sub_id: int, invite_id: int) -> None:
    delete_path = EMPLOYEE_INVITATION_DELETE_PATH.format(
        sub_id=int(sub_id),
        invite_id=int(invite_id),
    )
    response = lk_api.delete(delete_path)
    assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT, HTTPStatus.NOT_FOUND), (
        f"Delete invitation failed for invite_id={invite_id}: {response.status_code} {response.text}"
    )

    def _absent():
        response = accounts_list(lk_api, account_id=int(invite_id))
        if response.status_code == HTTPStatus.NO_CONTENT:
            return True
        if response.status_code != HTTPStatus.OK:
            return None
        items = response.json() if response.text else []
        if not isinstance(items, list):
            return None
        return True if find_account_in_list(items, int(invite_id)) is None else None

    deleted = wait_until(_absent, timeout_s=90, step_s=3)
    assert deleted is True, f"Employee/account id={invite_id} is still visible after delete"


def _resolve_account_card_id(lk_api, account_id: int) -> int | None:
    def _probe():
        response = accounts_list(lk_api, account_id=account_id)
        if response.status_code != HTTPStatus.OK:
            return None
        items = response.json() if response.text else []
        if not isinstance(items, list):
            return None
        found = find_account_in_list(items, account_id)
        if not found:
            return None
        card = found.get("card") or {}
        card_id = card.get("id")
        return int(card_id) if card_id else None

    return wait_until(_probe, timeout_s=60, step_s=3)


def _create_employee_invitation(
    lk_api,
    *,
    subscription_id: int,
    company_id: int,
    email: str,
    first_name: str,
    last_name: str,
    phone: str,
    position: str = "Director",
):
    payload = {
        "Email": email,
        "FirstName": first_name,
        "LastName": last_name,
        "CompanyID": company_id,
        "Phone": phone,
        "Position": position,
        "IsAcceptAdvertising": False,
    }
    response = lk_api.post(f"/Subscriptions/{subscription_id}/invitation", json=payload)
    assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED), (
        f"Create invitation failed: {response.status_code} {response.text}"
    )
    invite_id = int(response.json()["id"])
    card_id = _resolve_account_card_id(lk_api, invite_id)
    return {
        "invite_id": invite_id,
        "account_id": invite_id,
        "card_id": card_id,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone,
        "position": position,
    }


def _bulk_employee_flow(
    lk_api,
    *,
    subscription_id: int,
    company_id: int,
    count: int,
    email_prefix: str,
    first_prefix: str,
    phone_prefix: str,
    target_company_id: int | None = None,
):
    created = []
    base_ts = int(__import__("time").time())
    for idx in range(count):
        created.append(
            _create_employee_invitation(
                lk_api,
                subscription_id=subscription_id,
                company_id=company_id,
                email=f"{email_prefix}_{subscription_id}_{idx}_{base_ts}@mail.com",
                first_name=f"{first_prefix}_{idx}_{base_ts}",
                last_name="Employee",
                phone=f"{phone_prefix}{idx:04d}",
            )
        )

    return {
        "subscription_id": subscription_id,
        "company_id": company_id,
        "target_company_id": target_company_id,
        "created": created,
        "deleted_ids": set(),
    }


@pytest.fixture(scope="module")
def employee_addphoto_flow(lk_api, cfg):
    subscription_id = int(cfg["subscription_id"])
    company_id = int(cfg["company_id_create"])

    uniq = int(__import__("time").time())
    body = {
        "Email": f"autotest_{subscription_id}_{uniq}@mail.com",
        "FirstName": "AT_Photo",
        "LastName": "Employee",
        "CompanyID": company_id,
        "Phone": "89990001122",
        "IsAcceptAdvertising": False,
    }

    response = lk_api.post(f"/Subscriptions/{subscription_id}/invitation", json=body)
    assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED), response.text

    invite_id = int(response.json()["id"])
    account_id = invite_id
    card_id = _resolve_account_card_id(lk_api, account_id)
    assert card_id is not None, f"Card id not found for invited account {account_id}"

    attachment_ids: list[int] = []
    for idx in range(5):
        attachment_id = upload_generated_image(lk_api, cfg, label=f"employee_photo_{idx}")
        attachment_ids.append(attachment_id)

    ctx = {
        "subscription_id": subscription_id,
        "invite_id": invite_id,
        "account_id": account_id,
        "card_id": card_id,
        "attachment_ids": attachment_ids,
        "deleted": False,
    }

    yield ctx

    if not ctx.get("deleted"):
        _safe_delete_invitation(lk_api, subscription_id, invite_id)


@pytest.fixture(scope="module")
def employee_employment_export_flow(lk_api, cfg):
    subscription_id = int(cfg["subscription_id"])
    company_id_create = int(cfg["company_id_create"])

    first_name = rand_word("AT_Exp_FN", 6)
    last_name = rand_word("AT_Exp_LN", 6)
    email = rand_email(domain="mail.com")
    phone = "+7" + rand_word("9", 9).replace("_", "")[:10]

    payload = {
        "Email": email,
        "FirstName": first_name,
        "LastName": last_name,
        "CompanyID": company_id_create,
        "Phone": phone,
        "Position": "Director",
        "IsAcceptAdvertising": False,
    }

    response = lk_api.post(f"/Subscriptions/{subscription_id}/invitation", json=payload)
    assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED), (
        f"Create failed ({response.status_code}): {response.text}"
    )

    data = response.json() if response.text else {}
    invite_id = data.get("id")
    assert invite_id, f"No id in response: {data}"

    invite_id_int = int(invite_id)
    ctx = {
        "subscription_id": subscription_id,
        "company_id_create": company_id_create,
        "invite_id": invite_id_int,
        "account_id": invite_id_int,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "payload": payload,
        "deleted": False,
    }

    yield ctx

    if not ctx.get("deleted"):
        _safe_delete_invitation(lk_api, subscription_id, invite_id_int)


@pytest.fixture(scope="module")
def employee_flow_ctx():
    ctx = {
        "invite_id": None,
        "email": None,
        "deleted": False,
    }
    yield ctx


@pytest.fixture(scope="module")
def employee_invite_card_flow(lk_api, cfg):
    subscription_id = int(cfg["subscription_id"])
    company_id = int(cfg["company_id_create"])

    email = rand_email(domain="mail.com")
    phone = rand_phone_ru8()

    first = rand_word("AT_First", 6)
    last = rand_word("AT_Last", 6)
    position = rand_word("AT_Pos", 6)

    create_body = {
        "Email": email,
        "FirstName": first,
        "LastName": last,
        "CompanyID": company_id,
        "Phone": phone,
        "Position": position,
        "IsAcceptAdvertising": False,
    }

    with allure.step(f"POST /Subscriptions/{subscription_id}/invitation"):
        response = lk_api.post(f"/Subscriptions/{subscription_id}/invitation", json=create_body)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED), (
            f"Create invitation failed: {response.status_code} {response.text}"
        )

    data = response.json() if response.text else {}
    invite_id = data.get("id")
    assert invite_id, f"Create invitation: no id in response: {data}"

    invite_id_int = int(invite_id)
    account_id = invite_id_int
    card_id = _resolve_account_card_id(lk_api, account_id)
    assert card_id is not None, f"Card id not found for invited account {account_id}"

    new_name = rand_word("AT_CardName", 8)
    new_first = rand_word("AT_FN", 6)
    new_last = rand_word("AT_LN", 6)
    new_middle = rand_word("AT_MN", 6)
    new_self = "Self info " + rand_word("AT_Self", 10)
    new_position = rand_word("AT_Pos2", 6)

    updated = {
        "name": new_name,
        "first": new_first,
        "last": new_last,
        "middle": new_middle,
        "self": new_self,
        "position": new_position,
        "company_id": company_id,
    }

    put_body = {
        "Name": new_name,
        "Culture": "ru-RU",
        "IsPrimary": True,
        "Person": {
            "FirstName": new_first,
            "LastName": new_last,
            "MiddleName": new_middle,
            "SelfInfo": new_self,
        },
        "Employment": {
            "Position": new_position,
            "CompanyID": company_id,
        },
    }

    ctx = {
        "subscription_id": subscription_id,
        "company_id": company_id,
        "invite_id": invite_id_int,
        "account_id": account_id,
        "card_id": card_id,
        "created": {
            "email": email,
            "first": first,
            "last": last,
            "phone": phone,
            "position": position,
        },
        "updated": updated,
        "put_body": put_body,
        "deleted": False,
    }

    yield ctx

    if not ctx.get("deleted"):
        _safe_delete_invitation(lk_api, subscription_id, invite_id_int)


@pytest.fixture(scope="module")
def employee_stat_export_flow(lk_api, cfg):
    sub_id = int(cfg["subscription_id"])
    company_id_create = int(cfg["company_id_create"])

    payload = {
        "Email": rand_email(domain="mail.com"),
        "FirstName": rand_word("AT_Stat_FN", 6),
        "LastName": rand_word("AT_Stat_LN", 6),
        "CompanyID": company_id_create,
        "Phone": "+7" + rand_word("9", 12).replace("_", "")[:10],
        "Position": "Director",
        "IsAcceptAdvertising": False,
    }

    create_path = EMPLOYEE_INVITATION_CREATE_PATH.format(sub_id=sub_id)

    with allure.step(f"Create invitation: POST {create_path}"):
        allure.attach(str(payload), "invitation_payload", allure.attachment_type.TEXT)

        response = lk_api.post(create_path, json=payload)
        allure.attach(str(response.status_code), "create_status", allure.attachment_type.TEXT)
        allure.attach(response.text or "", "create_response_text", allure.attachment_type.TEXT)

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED), (
            f"Create failed ({response.status_code}): {response.text}"
        )

        data = response.json() if response.text else {}
        invite_id = data.get("id")
        assert invite_id, f"No id in response: {data}"

    invite_id_int = int(invite_id)

    ctx = {
        "subscription_id": sub_id,
        "company_id_create": company_id_create,
        "invite_id": invite_id_int,
        "account_id": invite_id_int,
        "email": payload["Email"],
        "first_name": payload["FirstName"],
        "deleted": False,
        "export_path": None,
        "date_from": None,
        "date_till": None,
    }

    yield ctx

    if not ctx.get("deleted"):
        _safe_delete_invitation(lk_api, sub_id, invite_id_int)


@pytest.fixture(scope="module")
def created_employee(lk_api, cfg, employee_flow_ctx) -> int:
    sub_id = int(cfg["subscription_id"])
    company_id_create = int(cfg["company_id_create"])

    email = rand_email(domain="tt.tt")
    employee_flow_ctx["email"] = email

    payload = {
        "Email": email,
        "FirstName": rand_word("AT_Nikita", 6),
        "LastName": rand_word("AT_Test", 6),
        "CompanyID": company_id_create,
        "Phone": rand_phone_ru8(),
        "Position": "Director",
        "IsAcceptAdvertising": False,
    }

    create_path = EMPLOYEE_INVITATION_CREATE_PATH.format(sub_id=sub_id)
    with allure.step(f"POST {create_path} (CompanyID={company_id_create})"):
        response = lk_api.post(create_path, json=payload)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED), (
            f"Create failed: {response.status_code} {response.text}"
        )
        data = response.json() if response.text else {}
        invite_id = data.get("id")
        assert invite_id, f"No id in response: {data}"

    invite_id_int = int(invite_id)
    employee_flow_ctx["invite_id"] = invite_id_int

    yield invite_id_int

    if not employee_flow_ctx.get("deleted"):
        _safe_delete_invitation(lk_api, sub_id, invite_id_int)


@pytest.fixture(scope="module")
def employee_hide_flow(lk_api, cfg):
    subscription_id = int(cfg["subscription_id"])
    company_id = int(cfg["company_id_create"])
    ctx = _bulk_employee_flow(
        lk_api,
        subscription_id=subscription_id,
        company_id=company_id,
        count=3,
        email_prefix="autotest_hide",
        first_prefix="AT_Hide",
        phone_prefix="8999000",
    )
    yield ctx
    for emp in ctx["created"]:
        invite_id = emp["invite_id"]
        if invite_id not in ctx["deleted_ids"]:
            _safe_delete_invitation(lk_api, subscription_id, invite_id)


@pytest.fixture(scope="module")
def employee_hide_show_flow(lk_api, cfg):
    subscription_id = int(cfg["subscription_id"])
    company_id = int(cfg["company_id_create"])
    ctx = _bulk_employee_flow(
        lk_api,
        subscription_id=subscription_id,
        company_id=company_id,
        count=3,
        email_prefix="autotest_hide_show",
        first_prefix="AT_HideShow",
        phone_prefix="8999111",
    )
    yield ctx
    for emp in ctx["created"]:
        invite_id = emp["invite_id"]
        if invite_id not in ctx["deleted_ids"]:
            _safe_delete_invitation(lk_api, subscription_id, invite_id)


@pytest.fixture(scope="module")
def employee_copyincompany_flow(lk_api, cfg):
    subscription_id = int(cfg["subscription_id"])
    source_company_id = int(cfg["company_id_create"])
    target_company_id = int(cfg["company_id_target"])
    ctx = _bulk_employee_flow(
        lk_api,
        subscription_id=subscription_id,
        company_id=source_company_id,
        count=4,
        email_prefix="autotest_copy",
        first_prefix="AT_Copy",
        phone_prefix="8999222",
        target_company_id=target_company_id,
    )
    yield ctx
    for emp in ctx["created"]:
        invite_id = emp["invite_id"]
        if invite_id not in ctx["deleted_ids"]:
            _safe_delete_invitation(lk_api, subscription_id, invite_id)


@pytest.fixture(scope="module")
def employee_moveincompany_flow(lk_api, cfg):
    subscription_id = int(cfg["subscription_id"])
    source_company_id = int(cfg["company_id_create"])
    target_company_id = int(cfg["company_id_target"])

    created = []
    base_ts = int(__import__("time").time())
    for idx in range(4):
        first_name = f"AT_MoveFN_{idx}_{base_ts}"
        created.append(
            _create_employee_invitation(
                lk_api,
                subscription_id=subscription_id,
                company_id=source_company_id,
                email=f"autotest_move_{subscription_id}_{idx}_{base_ts}@mail.com",
                first_name=first_name,
                last_name=f"AT_MoveLN_{idx}",
                phone=f"8999333{idx:04d}",
                position=f"AT_Pos_{idx}",
            )
        )

    ctx = {
        "subscription_id": subscription_id,
        "source_company_id": source_company_id,
        "target_company_id": target_company_id,
        "created": created,
        "deleted_ids": set(),
    }
    yield ctx
    for emp in ctx["created"]:
        invite_id = emp["invite_id"]
        if invite_id not in ctx["deleted_ids"]:
            _safe_delete_invitation(lk_api, subscription_id, invite_id)
