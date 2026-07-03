

class Payloads:

    @staticmethod
    def post_add_queries_binds_to_user_payload(name: str, query: str) -> list:
        payload = [
            {
                "Name": name,
                "QueryString": query
            }
        ]
        return payload

    @staticmethod
    def put_update_queries_payload(query_id: int, name: str, query: str) -> list:
        payload = [
            {
                "id": query_id,
                "Name": name,
                "QueryString": query
            }
        ]
        return payload

    @staticmethod
    def delete_queries_list_payloads(*args) -> list:
        return [*args]
