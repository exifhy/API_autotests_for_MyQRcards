
class Payloads:
    @staticmethod
    def build_cards_show_payload(*items: dict) -> list[dict]:
        return [
            {
                "AccountID": int(item["AccountID"]),
                "CardID": int(item["CardID"]),
            }
            for item in items
        ]
