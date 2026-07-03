

class Payloads:

    @staticmethod
    def post_role_task_list_queries_payload(role_id: int, *data: int | tuple) -> list:
        payload = [
            {
                "roleID": role_id,
                "data": [
                    *data
                ]
            }
        ]
        return payload

    @staticmethod
    def delete_role_task_list_queries_payload(role_id: int, *data: int | tuple) -> list:
        payload = [
            {
                "roleID": role_id,
                "data": [
                    *data
                ]
            }
        ]
        return payload
