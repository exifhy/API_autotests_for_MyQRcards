

class Payloads:

    @staticmethod
    def put_update_task_types_payload(*data: dict) -> list:
        return [*data]

    @staticmethod
    def post_add_task_types_payload(*data: dict) -> list:
        return [*data]

    @staticmethod
    def delete_task_types_by_list_payload(*task_type_ids: dict) -> list:
        return [*task_type_ids]

    @staticmethod
    def post_add_work_types_to_task_types_by_list_payload(*work_types_ids: int) -> list:
        return [*work_types_ids]

    @staticmethod
    def delete_unbind_work_types_from_task_type_payload(*work_types_ids: int) -> list:
        return [*work_types_ids]

