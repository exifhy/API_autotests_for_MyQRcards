

class Payloads:

    @staticmethod
    def post_add_user_template_payload(*data: dict or tuple) -> list:
        return [*data]

    @staticmethod
    def put_update_user_template_payload(*data: dict or tuple) -> list:
        return [*data]

    @staticmethod
    def delete_user_templates_by_list_payload(*template_ids: int or tuple) -> list:
        return [*template_ids]
