

class Payloads:

    @staticmethod
    def delete_task_conversations_payload(
            task_id: int,
            *message_ids: int,
    ) -> list:
        payload = [
            {
                "taskID": task_id,
                "data": [
                    *message_ids
                ]
            }
        ]
        return payload

    @staticmethod
    def delete_remove_task_conversations_payload(
            task_id: int,
            *message_ids: int,
    ) -> list:
        payload = [
            {
                "taskID": task_id,
                "data": [
                    *message_ids
                ]
            }
        ]
        return payload
