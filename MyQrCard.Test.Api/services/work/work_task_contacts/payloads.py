

class Payloads:

    @staticmethod
    def post_add_contacts_to_task_payload(
            task_id: int,
            *contact_ids: int,
    ) -> list:
        payload = [
            {
                "taskID": task_id,
                "data": [
                    *contact_ids
                ]
            }
        ]
        return payload

    @staticmethod
    def delete_contacts_from_task_payload(
            task_id: int,
            *contact_ids: int,
    ) -> list:
        payload = [
            {
                "taskID": task_id,
                "data": [
                    *contact_ids
                ]
            }
        ]
        return payload
