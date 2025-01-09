

class Payloads:

    @staticmethod
    def put_update_completed_works_payload(task_id: int, *data: dict) -> list:
        payload = [
            {
                "taskID": task_id,
                "data": [
                    *data
                ]
            }
        ]
        return payload

    @staticmethod
    def post_add_completed_works_payload(task_id: int, *data: dict) -> list:
        payload = [
            {
                "taskID": task_id,
                "data": [
                    *data
                ]
            }
        ]
        return payload

    @staticmethod
    def delete_completed_works_by_list_payload(*completed_works_ids: int, task_id: int) -> list:
        payload = [
            {
                "taskID": task_id,
                "data": [
                    *completed_works_ids
                ]
            }
        ]
        return payload

