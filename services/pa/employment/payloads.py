

class Payloads:

    @staticmethod
    def add_employment_customers_payload(user_id: int, customer_org_unit_id: int, date: str) -> dict:
        payloads = {
            "userID": user_id,
            "data": [
                {
                    "OrgUnitID": customer_org_unit_id,
                    "DateFrom": date,
                    "DateTill": "9999-12-31",
                    "Position": None
                }
            ]
        }
        return payloads
