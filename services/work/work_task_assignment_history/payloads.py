

class Payloads:

    @staticmethod
    def add_new_task_assignment_history(user_id: int, task_id: int, date_start: str, date_end: str) -> list:
        payload = [
            {
                "userID": user_id,
                "taskID": task_id,
                "scheduledStartDateTime": date_start,
                "scheduledFinishDateTime": date_end,
                "isPostponedNotification": True
            }
        ]
        return payload

    @staticmethod
    def add_new_task_assignment_history_payload(user_id: int, task_id: int, date_start: str, date_end: str) -> list:
        payload = [
            {
                "userID": user_id,
                "taskID": task_id,
                "scheduledStartDateTime": date_start,
                "scheduledFinishDateTime": date_end
            }
        ]
        return payload
