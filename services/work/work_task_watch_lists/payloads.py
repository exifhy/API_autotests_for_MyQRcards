

class Payloads:

    @staticmethod
    def post_add_task_watch_lists_payload(task_id: int, user_id: int) -> list:
        payload = [
            {
                "taskID": task_id,
                "data": [
                    user_id
                ]
            }
        ]
        return payload

    @staticmethod
    def delete_task_watch_lists_payload(task_id: int, user_id: int) -> list:
        payload = [
            {
                "taskID": task_id,
                "data": [
                    user_id
                ]
            }
        ]
        return payload
