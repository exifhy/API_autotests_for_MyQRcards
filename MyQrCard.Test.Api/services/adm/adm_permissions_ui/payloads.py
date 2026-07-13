

class Payloads:

    @staticmethod
    def post_add_permissions_ui_payload(*data: dict or tuple) -> list:
        return [*data]

    @staticmethod
    def put_update_permissions_ui_payload(*data: dict or tuple) -> list:
        return [*data]

    @staticmethod
    def delete_permissions_ui_by_list_payload(*data: int or tuple) -> list:
        return [*data]
