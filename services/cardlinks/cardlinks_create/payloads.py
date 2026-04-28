
class Payloads:
    @staticmethod
    def build_cardlinks_create_payload(*, custom_cardlink_id: str, is_default: bool = False) -> dict:
        return {
            "IsDefault": bool(is_default),
            "CustomCardLinkID": str(custom_cardlink_id),
        }
