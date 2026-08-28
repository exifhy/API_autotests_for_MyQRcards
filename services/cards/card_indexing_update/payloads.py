
class Payloads:
    @staticmethod
    def build_card_indexing_payload(is_indexable: bool) -> dict:
        return {
            "isIndexable": is_indexable,
        }
