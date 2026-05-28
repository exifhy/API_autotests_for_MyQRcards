
class Payloads:
    @staticmethod
    def build_accounts_cards_delete_many_payload(*, account_id: int, card_ids: list[int]) -> list[dict]:
        return [
            {
                "AccountID": int(account_id),
                "CardID": int(card_id),
            }
            for card_id in card_ids
        ]
