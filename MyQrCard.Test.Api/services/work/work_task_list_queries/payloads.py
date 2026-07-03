

class Payloads:

    @staticmethod
    def post_task_list_queries_payload(name: str, params: str) -> list:
        payload = [
            {
                "Name": name,
                "QueryString": params
            }
        ]
        return payload

    @staticmethod
    def put_task_list_queries_payload(query_id: int, name: str, params: str) -> list:
        payload = [
            {
                "id": query_id,
                "Name": name,
                "QueryString": params
            }
        ]
        return payload

    @staticmethod
    def delete_task_list_queries_payload(*query_ids: int) -> list:
        return [*query_ids]

    @staticmethod
    def delete_remove_task_list_queries_payload(*query_ids: int) -> list:
        return [*query_ids]

