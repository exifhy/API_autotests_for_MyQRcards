
class Payloads:
    @staticmethod
    def build_cardlink_update_payload(*, card_link_id: str, card_id: int, is_default: bool = True) -> dict:
        return {
            "CardLinkID": card_link_id,
            "CardID": int(card_id),
            "IsDefault": 1 if is_default else 0,
        }
