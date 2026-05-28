from src.utils.randoms import rand_word


class Payloads:
    @staticmethod
    def build_attribute_create_payload(attribute_type_id: int = 1) -> list[dict]:
        return [
            {
                "attributeTypeID": attribute_type_id,
                "name": rand_word("AT_Attr", 8),
            }
        ]
