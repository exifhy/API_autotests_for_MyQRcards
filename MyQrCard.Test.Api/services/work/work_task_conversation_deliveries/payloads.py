

class Payloads:

    @staticmethod
    def put_task_conversation_deliveries_payload(task_id: int, conversation_id: int) -> list:
        payload = [
            {
                "taskID": task_id,
                "data": [
                    {
                        "id": conversation_id
                    }
                ]
            }
        ]
        return payload
