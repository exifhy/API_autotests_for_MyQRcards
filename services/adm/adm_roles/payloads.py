

class Payloads:

    @staticmethod
    def post_add_roles_payload(*data: dict or tuple) -> list:
        return [*data]

    @staticmethod
    def post_copy_roles_payload(*data: dict or tuple) -> list:
        return [*data]

    @staticmethod
    def put_update_roles_payload(*data: dict or tuple) -> list:
        return [*data]

    @staticmethod
    def delete_roles_by_list_payload(*data: int or tuple) -> list:
        return [*data]
