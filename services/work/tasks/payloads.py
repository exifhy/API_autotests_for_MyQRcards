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
