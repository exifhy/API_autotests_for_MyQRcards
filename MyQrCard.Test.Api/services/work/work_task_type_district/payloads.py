

class Payloads:

    @staticmethod
    def put_update_task_type_district_payload(task_type_id: int, *district_ids: int) -> list:
        payload = [
            {
                "data": [
                    *district_ids
                ],
                "taskTypeID": task_type_id
            }
        ]
        return payload
