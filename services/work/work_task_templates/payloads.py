

class Payloads:

    @staticmethod
    def add_task_templates_payloads(
            template_name: str,
            templates_note: str,
            asset_id: int,
            task_type_id: str,
            work_type_id: str
    ) -> list:
        payloads = [
            {
                "name": template_name,
                "taskTypeID": task_type_id,
                "workTypeID": work_type_id,
                "criticalityID": "1",
                "code": None,
                "notes": templates_note,
                "estimatedTimeConsumptionMinutes": "",
                "estimatedCost": "",
                "requestMethodID": 1,
                "assetFilter": {
                    "assets": [asset_id]
                }
            }
        ]
        return payloads

    @staticmethod
    def put_update_task_templates_payloads(
            template_id: str,
            template_name: str,
            templates_note: str,
            asset_id: int,
            task_type_id: str,
            work_type_id: str,
            code_str: str
    ) -> list:
        payloads = [
            {
                "id": template_id,
                "name": template_name,
                "taskTypeID": task_type_id,
                "workTypeID": work_type_id,
                "criticalityID": "1",
                "code": code_str,
                "notes": templates_note,
                "estimatedTimeConsumptionMinutes": "",
                "estimatedCost": "",
                "requestMethodID": 1,
                "assetFilter": {
                    "assets": [asset_id]
                }
            }
        ]
        return payloads

    @staticmethod
    def delete_task_templates_payloads(task_templates_id: str) -> list:
        return [task_templates_id]

    @staticmethod
    def bind_employee_to_template_payloads(*user_ids: int) -> list:
        return [*user_ids]

    @staticmethod
    def add_task_templates_for_schedules_payloads(schedule_id: int) -> list:
        return [schedule_id]

