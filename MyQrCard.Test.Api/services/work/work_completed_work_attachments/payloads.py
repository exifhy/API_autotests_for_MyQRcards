

class Payloads:

    @staticmethod
    def post_completed_work_attachments_payload(
            task_id: int,
            completed_work_id: int,
            attachment_id: int
    ) -> list:
        payload = [
            {
                "taskID": task_id,
                "data": [
                    {
                        "completedWorkID": completed_work_id,
                        "attachmentID": attachment_id
                    }
                ]
            }
        ]
        return payload

    @staticmethod
    def delete_completed_work_attachments_payload(
            task_id: int,
            completed_work_id: int,
            attachment_id: int
    ) -> list:
        payload = [
            {
                "taskID": task_id,
                "data": [
                    {
                        "completedWorkID": completed_work_id,
                        "attachmentID": attachment_id
                    }
                ]
            }
        ]
        return payload
