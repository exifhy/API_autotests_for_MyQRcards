

class Payloads:

    @staticmethod
    def post_add_user_asset_list_queries_by_list_payload(*queries_ids: int or tuple) -> list:
        return [*queries_ids]

    @staticmethod
    def delete_user_asset_list_queries_by_list_payload(*queries_ids: int or tuple) -> list:
        return [*queries_ids]

    @staticmethod
    def post_add_user_asset_list_queries_payload(user_id: int, *queries_ids: int or tuple) -> list:
        payload = [
            {
                "data": [
                    *queries_ids
                ],
                "userID": user_id
            }
        ]
        return payload

    @staticmethod
    def delete_user_asset_list_queries_payload(user_id: int, *queries_ids: int or tuple) -> list:
        payload = [
            {
                "data": [
                    *queries_ids
                ],
                "userID": user_id
            }
        ]
        return payload
