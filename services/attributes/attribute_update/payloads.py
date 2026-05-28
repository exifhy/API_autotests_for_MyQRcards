from src.utils.randoms import rand_word


class Payloads:
    @staticmethod
    def build_attribute_update_payload(attribute_id: int, **_) -> list[dict]:
        return [
            {
                "id": attribute_id,
                "name": rand_word("AT_Attr_upd", 8),
            }
        ]
