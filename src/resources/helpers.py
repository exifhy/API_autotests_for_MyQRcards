from __future__ import annotations

from src.utils.randoms import rand_email, rand_word


def find_account_in_list(items: list, account_id: int):
    for it in items or []:
        if isinstance(it, dict) and int(it.get("id", -1)) == int(account_id):
            return it
    return None


def find_company_in_list(items: list, company_id: int | None = None, name: str | None = None):
    for it in items or []:
        if not isinstance(it, dict):
            continue
        if company_id is not None and int(it.get("id", -1)) == int(company_id):
            return it
        if name is not None and (it.get("name") == name or it.get("Name") == name):
            return it
    return None


def is_logo_removed(company_json: dict) -> bool:
    logo = company_json.get("logo")
    logo_att = company_json.get("logoAttachmentID") or company_json.get("LogoAttachmentID")

    if logo is None:
        return True
    if logo_att is None:
        return True
    if str(logo_att).strip() in ("0", ""):
        return True
    if isinstance(logo, dict) and not logo.get("id"):
        return True
    return False


def is_background_removed(designsettings_json: dict) -> bool:
    bg_id = designsettings_json.get("backgroundAttachmentID") or designsettings_json.get("BackgroundAttachmentID")
    return (bg_id is None) or (str(bg_id).strip() in ("0", ""))


def build_company_create_payload(*, logo_id: int | None = None) -> dict:
    payload = {
        "Name": rand_word("Api_tests_company", 8),
        "Phone": "+78129875643",
        "Fax": "+78129875643",
        "Email": rand_email(domain="tt.tt"),
        "SiteUrl": "https://www.test.tt",
        "FoundedYear": 2018,
        "Activity": "Testing, Testing, Testing",
        "Customers": "Testers, Testers",
        "Location": {
            "Country": "Russia",
            "PostalCode": "198198",
            "Region": "Leningradskaya oblast",
            "Address": "Murino, Shuvalova 9",
            "Notes": "13 app.",
            "Latitude": "32.987656",
            "Longitude": "32.987656",
        },
        "SocialNetworks": [
            {"SocialNetworkID": 1, "ContactUrl": "https://cn.com/test"},
            {"SocialNetworkID": 7, "ContactUrl": "tg://resolve?domain=zdarova"},
            {"SocialNetworkID": 8, "ContactUrl": "https://wa.me/+89452342323"},
            {"SocialNetworkID": 9, "ContactUrl": "viber://chat?number=86767575676"},
            {"SocialNetworkID": 19, "ContactUrl": "86767575676"},
        ],
    }
    if logo_id is not None:
        payload["logoAttachmentID"] = int(logo_id)
    return payload


def parse_card_v2_minimal(card_v2: dict) -> dict:
    person = card_v2.get("person") or card_v2.get("Person") or {}
    return {
        "lastName": person.get("lastName") or person.get("LastName"),
        "selfInfo": person.get("selfInfo") or person.get("SelfInfo"),
        "_raw": card_v2,
    }
