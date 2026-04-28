from services.cards.card_by_id.api_card_by_id import CardByIdAPI
from services.cards.card_create.api_card_create import CardCreateAPI
from src.support.waiter import wait_until
from http import HTTPStatus


def create_card_and_fill_flow(state: dict, *, subscription_id: int, company_id: int) -> None:
    created = CardCreateAPI().create_card(
        subscription_id=subscription_id,
        company_id=company_id,
    )
    assert created.id is not None, "Card create returned empty id"
    state["card_id"] = int(created.id)

    fetched = CardByIdAPI().get_card_by_id(state["card_id"])
    assert fetched.accountID is not None, "Created card has empty accountID"
    state["account_id"] = int(fetched.accountID)


def wait_accounts_leadgen_form_present(
    lk_api,
    *,
    account_id: int,
    card_id: int,
    expected_form_text: str,
    expected_button_text: str,
    expected_field_template_id: int,
    timeout_s: int = 60,
    step_s: int = 3,
):
    path = f"/accounts/{int(account_id)}/cards/{int(card_id)}/leadgenforms"

    def _present():
        response = lk_api.get(path)
        if response.status_code not in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT):
            return None
        items = response.json() if response.text else []
        if not isinstance(items, list):
            return None

        for item in items:
            if not isinstance(item, dict):
                continue
            if item.get("formText") != expected_form_text:
                continue
            if item.get("buttonText") != expected_button_text:
                continue
            fields = item.get("fields") or []
            if any(
                isinstance(field, dict) and int(field.get("fieldTemplateID", 0)) == int(expected_field_template_id)
                for field in fields
            ):
                return item
        return None

    return wait_until(_present, timeout_s=timeout_s, step_s=step_s)


def social_contact_url(name: str, attribute_id: int) -> str:
    slug = "".join(ch.lower() if ch.isalnum() else "-" for ch in name).strip("-") or f"social-{attribute_id}"
    return f"https://social.local/{slug}/{attribute_id}"


def build_card_attributes_socials_body(social_attributes: list[dict]) -> tuple[list[dict], dict[str, str]]:
    expected_urls = {
        item["name"]: social_contact_url(item["name"], int(item["id"]))
        for item in social_attributes
    }

    body = [
        {
            "AttributeID": int(item["id"]),
            "Name": item["name"],
            "SortOrder": index,
            "IsEnabled": True,
            "Value": [expected_urls[item["name"]]],
        }
        for index, item in enumerate(social_attributes, start=1)
    ]
    return body, expected_urls


def wait_card_socials_in_0852(
    lk_api,
    *,
    account_id: int,
    card_id: int,
    expected_urls_by_name: dict[str, str],
    timeout_s: int = 90,
    step_s: int = 3,
):
    path = f"/accounts/{int(account_id)}/cards/{int(card_id)}/attributes/"

    def _present():
        response = lk_api.get(path)
        if response.status_code != HTTPStatus.OK:
            return None
        items = response.json() if response.text else []
        if not isinstance(items, list):
            return None

        for expected_name, expected_url in expected_urls_by_name.items():
            found = False
            for item in items:
                if not isinstance(item, dict):
                    continue
                attr = item.get("attribute") or {}
                card_attr = item.get("cardAttribute") or {}
                name = str(attr.get("name") or card_attr.get("name") or "").strip()
                values = [str(value) for value in (item.get("values") or []) if value is not None]
                if name == expected_name and expected_url in values:
                    found = True
                    break
            if not found:
                return None
        return items

    return wait_until(_present, timeout_s=timeout_s, step_s=step_s)
