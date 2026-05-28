import random
import string


def rand_word(prefix: str, n: int = 8) -> str:
    tail = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))
    return f"{prefix}_{tail}"


def rand_space_text(n: int = 30) -> str:
    words = [
        "cosmos",
        "orbit",
        "star",
        "nebula",
        "comet",
        "galaxy",
        "quark",
        "photon",
        "supernova",
        "pulsar",
        "asteroid",
        "satellite",
    ]
    base = f"{random.choice(words)} {random.choice(words)} {random.choice(words)}"
    base += " " + rand_word("space", 6)
    return base[:n].ljust(n, "x")


def rand_hex_color() -> str:
    return "".join(random.choice("0123456789ABCDEF") for _ in range(6))


def rand_youtube_url() -> str:
    return f"https://youtube.com/{rand_word('video', 10)}"


def build_mobile_payload(*, now: int, name_prefix: str = "TestCard") -> dict:
    return {
        "Name": f"{name_prefix}_{now}",
        "Culture": "ru-RU",
        "IsPrimary": True,
        "Person": {
            "FirstName": f"FN_{now}",
            "LastName": f"LN_{now}",
            "MiddleName": f"MN_{now}",
        },
        "Employment": {
            "Position": None,
            "Activity": None,
            "Phone": None,
            "Email": None,
            "CompanyID": None,
        },
    }


def build_mobile_random_payload(*, name_prefix: str = "Card") -> dict:
    return {
        "Name": rand_word(name_prefix),
        "Culture": "ru-RU",
        "IsPrimary": True,
        "Person": {
            "FirstName": rand_word("FN"),
            "LastName": rand_word("LN"),
            "MiddleName": rand_word("MN"),
            "Attachments": None,
        },
        "Employment": {
            "Position": None,
            "Activity": None,
            "Phone": None,
            "Email": None,
            "CompanyID": None,
        },
    }


def build_mobile_gallery_attachments(attachment_ids: list[int]) -> list[dict]:
    return [
        {"attachmentID": int(attachment_id), "sortOrder": index}
        for index, attachment_id in enumerate(attachment_ids, start=1)
    ]


def build_mobile_update_payload(*, attachment_ids: list[int], name: str = "TestUpd") -> dict:
    return {
        "Name": name,
        "Culture": "ru-RU",
        "IsPrimary": True,
        "Person": {
            "FirstName": "Test",
            "LastName": "Test",
            "MiddleName": "Test",
            "selfInfo": "About",
            "Attachments": build_mobile_gallery_attachments(attachment_ids),
            "SocialNetworks": [
                {
                    "SocialNetworkID": 1,
                    "ContactUrl": "https://cn.com/test",
                }
            ],
        },
        "Employment": {
            "Position": None,
            "Activity": None,
            "Phone": None,
            "Email": None,
            "CompanyID": None,
        },
    }


def build_mobile_avatar_update_payload(*, attachment_id: int) -> dict:
    return {
        "name": rand_word("Ha"),
        "culture": "ru-RU",
        "isPrimary": False,
        "person": {
            "firstName": rand_word("Hd"),
            "lastName": rand_word("Ln"),
            "middleName": rand_word("Mn"),
            "selfInfo": rand_word("About"),
            "attachments": [
                {
                    "attachmentId": int(attachment_id),
                    "sortOrder": 1,
                }
            ],
        },
        "employment": {
            "position": "",
            "companyId": None,
        },
    }


def build_mobile_attribute_body(
    *,
    attribute_id: int,
    name: str,
    sort_order: int,
    value: list,
    is_enabled: bool = True,
    attachment_id: int | None = None,
    attribute_form_id=None,
) -> list[dict]:
    item = {
        "AttributeID": attribute_id,
        "Name": name,
        "SortOrder": sort_order,
        "Value": value,
        "IsEnabled": is_enabled,
    }
    if attachment_id is not None:
        item["AttachmentID"] = int(attachment_id)
    if attribute_form_id is not None or "YouTube" == name:
        item["AttributeFormID"] = attribute_form_id
    return [item]


def build_mobile_designsettings_body(*, color: str, background_attachment_id: int | None = None) -> dict:
    return {
        "Color": color,
        "QRColor": None,
        "BackgroundColor": None,
        "ForegroundColor": None,
        "BackgroundAttachmentID": background_attachment_id,
    }
