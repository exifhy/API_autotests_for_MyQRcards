

class Payloads:

    @staticmethod
    def post_add_user_task_favourites_payload(*task_ids: int) -> list:
        return [*task_ids]

    @staticmethod
    def delete_task_from_user_favourites_payload(*task_ids: int) -> list:
        return [*task_ids]
