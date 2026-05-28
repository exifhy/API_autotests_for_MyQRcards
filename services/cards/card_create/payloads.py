import time


class Payloads:
    @staticmethod
    def build_card_create_payload(*, subscription_id: int, company_id: int) -> dict:
        now = int(time.time())
        return {
            "subscriptionID": int(subscription_id),
            "name": f"AT_Card_{now}",
            "culture": "ru-RU",
            "isPrimary": False,
            "themeID": 1,
            "person": {
                "firstName": f"FN_{now}",
                "lastName": f"LN_{now}",
                "middleName": f"MN_{now}",
            },
            "isHidden": False,
            "employment": {
                "companyID": int(company_id),
            },
        }
