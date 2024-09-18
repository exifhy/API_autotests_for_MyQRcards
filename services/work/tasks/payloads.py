from datetime import datetime


class Payloads:

    @staticmethod
    def add_task_payload(number: str, note: str, date: str, **kwargs) -> dict:
        payload = {
            "CriticalityID": "1",
            "EstimatedCostCurrencyID": 1,
            "FaultTimestamp": date,
            "RequestMethodID": 1,
            "RequestedFinishDateTime": date,
            "RequestedStartDateTime": date,
            "TaskTypeID": "7",
            "notes": note,
            "number": number,
            **kwargs
        }
        return payload
