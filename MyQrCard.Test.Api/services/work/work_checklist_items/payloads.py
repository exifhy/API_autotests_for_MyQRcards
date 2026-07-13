

class Payloads:

    @staticmethod
    def post_add_checklist_items_payload(checklist_id: int, *args) -> list:
        payload = [
            {
                "checkListID": checklist_id,
                "data": [*args]
            }
        ]
        return payload

    @staticmethod
    def delete_checklist_items_payload(*args) -> list:
        return [*args]
