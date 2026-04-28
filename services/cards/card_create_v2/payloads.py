import time


class Payloads:
    @staticmethod
    def build_card_create_v2_payload(*, attachment_id: int | None = None) -> dict:
        now = int(time.time())
        payload = {
            "Name": f"AT_Card_V2_{now}",
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
        if attachment_id is not None:
            payload["Person"]["Attachments"] = [int(attachment_id)]
        return payload
