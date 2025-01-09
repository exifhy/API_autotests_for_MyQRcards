
class Payloads:

    @staticmethod
    def post_bind_attachments_to_task_payload(
            task_id: int,
            *attachment_ids: int
    ) -> list:
        payload = [
            {
                "taskID": task_id,
                "data": [*attachment_ids]
            }
        ]
        return payload

    @staticmethod
    def delete_unbind_attachments_from_task_payload(
            task_id: int,
            *attachment_ids: int
    ) -> list:
        payload = [
            {
                "taskID": task_id,
                "data": [*attachment_ids]
            }
        ]
        return payload
