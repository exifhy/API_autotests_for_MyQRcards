

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
            stage_ids: list[str],
            task_ids: list[int]
    ) -> list[dict]:
        payload = [
            {
                "taskStageID": stage_id,
                "TaskID": task_id
            }
            for stage_id, task_id in zip(stage_ids, task_ids)
        ]
        return payload

