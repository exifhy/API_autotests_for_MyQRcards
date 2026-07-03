

class Payloads:

    @staticmethod
    def post_add_checklists_payload(name: str, desc: str) -> list:
        payload = [
            {
                "name": name,
                "description": desc
            }
        ]
        return payload

    @staticmethod
    def put_update_checklists_payload(checklist_id: int, name: str, desc: str) -> list:
        payload = [
            {
                "id": checklist_id,
                "name": name,
                "description": desc
            }
        ]
        return payload

    @staticmethod
    def delete_checklists_payloads(*args) -> list:
        return [*args]

    @staticmethod
    def post_checklists_assign_payload(*asset_ids: int, work_type_id: int) -> dict:
        payload = {
            "assets": [*asset_ids],
            "workTypes": [work_type_id]
        }
        return payload

    @staticmethod
    def delete_checklists_assign_payload(*asset_ids: int, work_type_id: int) -> dict:
        payload = {
            "assets": [*asset_ids],
            "workTypes": [work_type_id]
        }
        return payload
