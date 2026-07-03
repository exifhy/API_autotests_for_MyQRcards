

class Payloads:

    @staticmethod
    def put_task_materials_payload(task_id: int, data: dict) -> list:
        payload = [
            {
                "taskID": task_id,
                "data": [
                    data
                ]
            }
        ]
        return payload

    @staticmethod
    def post_task_materials_payload(task_id: int, data: dict) -> list:
        payload = [
            {
                "taskID": task_id,
                "data": [
                    data
                ]
            }
        ]
        return payload

    @staticmethod
    def delete_task_materials_payload(task_id: int, *material_ids: int) -> list:
        payload = [
            {
                "taskID": task_id,
                "data": [
                    *material_ids
                ]
            }
        ]
        return payload

    @staticmethod
    def put_task_materials_take_on_payload(task_id: int, data: dict) -> list:
        payload = [
            {
                "taskID": task_id,
                "data": [
                    data
                ]
            }
        ]
        return payload

    @staticmethod
    def put_task_materials_take_off_payload(task_id: int, *material_ids: int) -> list:
        payload = [
            {
                "taskID": task_id,
                "data": [
                    *material_ids
                ]
            }
        ]
        return payload
