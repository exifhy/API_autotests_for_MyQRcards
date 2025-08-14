

class Payloads:

    @staticmethod
    def post_add_layout_template_payload(default: bool, name: str) -> dict:
        payload = {

        }
        return payload

    @staticmethod
    def put_update_layout_template_payload(default: bool, name: str) -> dict:
        payload = {

        }
        return payload

    @staticmethod
    def put_add_task_types_to_layout_template_payload(*task_types_ids: int or tuple) -> list:
        return [*task_types_ids]

    @staticmethod
    def delete_task_types_from_layout_template_payload(*task_types_ids: int or tuple) -> list:
        return [*task_types_ids]
