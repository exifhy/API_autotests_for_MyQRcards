

class Payloads:

    @staticmethod
    def post_add_task_skills_payload(task_id: int, *skill_ids: int):
        payload = [
            {
                "taskID": task_id,
                "data": [
                    *skill_ids
                ]
            }
        ]
        return payload

    @staticmethod
    def delete_task_skills_payload(task_id: int, *skill_ids: int):
        payload = [
            {
                "taskID": task_id,
                "data": [
                    *skill_ids
                ]
            }
        ]
        return payload
