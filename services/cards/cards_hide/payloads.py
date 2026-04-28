
class Payloads:
    @staticmethod
    def build_cards_hide_payload(*items: dict) -> list[dict]:
        return [
            {
                "AccountID": int(item["AccountID"]),
                "CardID": int(item["CardID"]),
            }
            for item in items
        ]
