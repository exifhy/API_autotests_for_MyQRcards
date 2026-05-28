from __future__ import annotations


def _norm(value: str | None) -> str:
    return (value or "").strip().lower()


def build_social_attrs_payload(
    *,
    telegram_id: int,
    whatsapp_id: int,
    telegram_url: str,
    whatsapp_url: str,
) -> list[dict]:
    return [
        {
            "AttributeID": int(telegram_id),
            "Name": "Telegram",
            "SortOrder": 2,
            "Value": [telegram_url],
            "IsEnabled": True,
            "AttributeFormID": None,
        },
        {
            "AttributeID": int(whatsapp_id),
            "Name": "WhatsApp",
            "SortOrder": 3,
            "Value": [whatsapp_url],
            "IsEnabled": True,
            "AttributeFormID": None,
        },
    ]


def extract_social_names_from_v2(card_v2: dict) -> set[str]:
    person = card_v2.get("person") or card_v2.get("Person") or {}
    socials = person.get("socialNetworks") or person.get("SocialNetworks") or []

    out: set[str] = set()
    if isinstance(socials, list):
        for item in socials:
            if isinstance(item, dict):
                out.add(_norm(item.get("name") or item.get("Name")))
    return out


def has_socials_in_0852(items: list, expected_names: set[str]) -> bool:
    seen = set()
    for item in items:
        attr = item.get("attribute") or item.get("Attribute") or {}
        name = _norm(attr.get("name") or attr.get("Name"))
        if name:
            seen.add(name)
    return expected_names.issubset(seen)
