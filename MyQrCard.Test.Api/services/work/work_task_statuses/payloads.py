

class Payloads:

    @staticmethod
    def post_add_task_statuses_payload(value: dict) -> list:
        return [value]

    @staticmethod
    def put_update_task_statuses_payload(value: dict) -> list:
        return [value]

    @staticmethod
    def delete_task_statuses_by_list_payload(*task_statuses_ids: int) -> list:
        return [*task_statuses_ids]
