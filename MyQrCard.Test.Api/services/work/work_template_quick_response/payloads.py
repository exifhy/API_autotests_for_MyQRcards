

class Payloads:

    @staticmethod
    def put_template_quick_response_payload(data: dict) -> list:
        return [data]

    @staticmethod
    def post_add_template_quick_response_payload(*data: dict) -> list:
        return [*data]

    @staticmethod
    def delete_template_quick_response_by_list_payload(*response_ids: int) -> list:
        return [*response_ids]

    @staticmethod
    def put_update_task_type_template_quick_response_by_list_payload(response_id: int, task_type_id: int) -> list:
        payload = [
            {
                "responseID": response_id,
                "taskTypes": [
                    task_type_id
                ]
            }
        ]
        return payload
