

class Payloads:

    @staticmethod
    def post_task_tags_payload(task_id: int, tags: str) -> list:
        payload = [
            {
                "taskID": task_id,
                "tags": [
                    tags
                ]
            }
        ]
        return payload

    @staticmethod
    def delete_task_tags_payload(task_id: int, tags: str) -> list:
        payload = [
            {
                "taskID": task_id,
                "tags": [
                    tags
                ]
            }
        ]
        return payload
