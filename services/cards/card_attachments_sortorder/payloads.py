
class Payloads:
    @staticmethod
    def build_card_attachments_sortorder_payload(*items: dict) -> list[dict]:
        return [
            {
                "attachmentID": int(item["attachmentID"]),
                "sortOrder": int(item["sortOrder"]),
            }
            for item in items
        ]
