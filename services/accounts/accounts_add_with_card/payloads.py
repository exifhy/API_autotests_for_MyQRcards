import time


class Payloads:
    @staticmethod
    def build_accounts_add_with_card_payload() -> dict:
        now = int(time.time())
        return {
            "firstName": "Test",
            "lastName": f"Auto_{now}",
            "email": f"autotest_addwithcard_{now}@example.com",
            "mobilePhone": f"+7999{now % 10000000:07d}",
            "companyName": "Autotest Company",
            "position": "QA",
            "isAcceptAdvertising": True,
        }
