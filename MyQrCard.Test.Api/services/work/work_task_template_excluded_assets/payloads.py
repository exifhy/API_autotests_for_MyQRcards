

class Payloads:

    @staticmethod
    def post_add_task_template_excluded_assets_payload(task_template_id: str, *asset_ids: int) -> list:
        payload = [
            {
                "taskTemplateID": task_template_id,
                "data": [
                    *asset_ids
                ]
            }
        ]
        return payload

    @staticmethod
    def delete_task_template_excluded_assets_payload(task_template_id: str, *asset_ids: int) -> list:
        payload = [
            {
                "taskTemplateID": task_template_id,
                "data": [
                    *asset_ids
                ]
            }
        ]
        return payload
