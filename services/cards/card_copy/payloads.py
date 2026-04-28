
class Payloads:
    @staticmethod
    def build_card_copy_payload(*items: dict) -> list[dict]:
        return [
            {
                "AccountID": int(item["AccountID"]),
                "CardID": int(item["CardID"]),
                "CompanyID": int(item["CompanyID"]),
            }
            for item in items
        ]
