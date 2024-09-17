

class Payloads:

    @staticmethod
    def add_actual_record_to_history_progress_task_by_stage_payload(
            stage_id: str,
            task_id: int
    ) -> dict:
        payload = {
            "taskStageID": stage_id,
            "TaskID": task_id
        }
        return payload

    @staticmethod
    def mass_movement_of_task_by_stage_payload(
            stage_id: str,
            task_id: int
    ) -> list:
        payload = [
            {
                "taskStageID": stage_id,
                "TaskID": task_id
            }
        ]
        return payload

