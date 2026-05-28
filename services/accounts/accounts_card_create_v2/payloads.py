import time


class Payloads:
    @staticmethod
    def build_accounts_card_create_v2_payload(*, subscription_id: int | None = None) -> dict:
        now = int(time.time())
        payload = {
            "Name": f"End_{now}",
            "Culture": "ru-RU",
            "IsPrimary": True,
            "Person": {
                "FirstName": "Test",
                "LastName": "Test",
                "MiddleName": "Test",
            },
        }
        if subscription_id is not None:
            payload["SubscriptionID"] = int(subscription_id)
        return payload
