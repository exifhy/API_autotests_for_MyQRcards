from datetime import datetime


class Payloads:

    @staticmethod
    def add_task_payload(
            criticality_id: str,
            number: str,
            note: str,
            task_type_id: str,
            date: str,
            **kwargs
    ) -> dict:
        payload = {
            "CriticalityID": criticality_id,
            "EstimatedCostCurrencyID": 1,
            "FaultTimestamp": date,
            "RequestMethodID": 1,
            "RequestedFinishDateTime": date,
            "RequestedStartDateTime": date,
            "TaskTypeID": task_type_id,
            "notes": note,
            "number": number,
            **kwargs
        }
        return payload

    @staticmethod
    def put_update_task_payload(
            number: str,
            note: str,
            date: str,
            **kwargs
    ) -> dict:
        payload = {
            "FaultTimestamp": date,
            "RequestedFinishDateTime": date,
            "RequestedStartDateTime": date,
            "notes": note,
            "number": number,
            **kwargs
        }
        return payload

    @staticmethod
    def post_add_conversation_to_task_payload(
            external: bool,
            value: str
    ) -> dict:
        payload = {
            "message": value,
            "isExternal": external,
            "attachments": []
        }
        return payload

    @staticmethod
    def post_add_checklists_to_task_payload(checklist_id: int) -> list:
        payload = [
            {
                "checkListID": checklist_id
            }
        ]
        return payload

    @staticmethod
    def delete_checklists_from_task_by_list_payload(*checklist_ids: int) -> list:
        return [*checklist_ids]
