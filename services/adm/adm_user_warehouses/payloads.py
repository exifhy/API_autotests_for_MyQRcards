

class Payloads:

    @staticmethod
    def post_add_warehouses_to_user_payload(user_id: int, *warehouses_ids: int or tuple) -> list:
        payload = [
            {
                "userID": user_id,
                "warehouseIDs": [
                    *warehouses_ids
                ]
            }
        ]
        return payload

    @staticmethod
    def delete_warehouses_from_user_payload(user_id: int, *warehouses_ids: int or tuple) -> list:
        payload = [
            {
                "userID": user_id,
                "warehouseIDs": [
                    *warehouses_ids
                ]
            }
        ]
        return payload
