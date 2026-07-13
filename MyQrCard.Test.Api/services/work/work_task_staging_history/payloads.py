

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

    @staticmethod
    def post_mass_movement_of_task_by_stage_batch_payload(
            guid, task_stage_ids: list[int], list_task_ids: list[list[int]]
    ) -> dict:
        """
        Создает тело запроса в нужном формате
        :param guid: строковый guid
        :param task_stage_ids: список taskStageID, например [1, 2, 3]
        :param list_task_ids: список списков tasks, например [[10], [20, 21], [30]]
        :return: словарь
        """
        if len(task_stage_ids) != len(list_task_ids):
            raise ValueError("Длина task_stage_ids и list_task_ids должна совпадать")
        payload = {
            "data": [
                {
                    "taskStageID": stage_id,
                    "tasks": list(map(str, task_id))
                }
                for stage_id, task_id in zip(task_stage_ids, list_task_ids)
            ],
            "concurrencyStamp": guid
        }
        return payload
