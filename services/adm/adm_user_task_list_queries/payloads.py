

class Payloads:

    @staticmethod
    def post_add_user_task_list_queries_payload(user_id: int, *task_list_queries_ids: int or tuple) -> list:
        payload = [
            {
                "data": [
                    *task_list_queries_ids
                ],
                "userID": user_id
            }
        ]
        return payload

    @staticmethod
    def delete_user_task_list_queries_payload(user_id: int, *task_list_queries_ids: int or tuple) -> list:
        payload = [
            {
                "data": [
                    *task_list_queries_ids
                ],
                "userID": user_id
            }
        ]
        return payload
