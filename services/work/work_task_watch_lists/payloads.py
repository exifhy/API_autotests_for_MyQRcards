

class Payloads:

    @staticmethod
    def post_add_task_watch_lists_payload(task_id: int, *user_ids: int) -> list:
        payload = [
            {
                "taskID": task_id,
                "data": [
                    *user_ids
                ]
            }
        ]
        return payload

    @staticmethod
    def delete_task_watch_lists_payload(task_id: int, *user_ids: int) -> list:
        payload = [
            {
                "taskID": task_id,
                "data": [
                    *user_ids
                ]
            }
        ]
        return payload
