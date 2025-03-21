

class Payloads:

    @staticmethod
    def put_update_task_type_routes_payload(*data: dict) -> list:
        return [*data]

    @staticmethod
    def post_add_task_type_routes_payload(*data: dict) -> list:
        return [*data]

    @staticmethod
    def delete_task_type_routes_by_list_payload(*routes_ids: int) -> list:
        return [*routes_ids]
