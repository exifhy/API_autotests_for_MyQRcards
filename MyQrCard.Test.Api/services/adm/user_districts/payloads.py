

class Payloads:

    @staticmethod
    def add_districts_to_user_payload(districts_id: int, user_id: int, schedule_id) -> dict:
        payload = {
            "data": [
                {
                    "districtID": districts_id,
                    "scheduleRuleID": schedule_id
                }
            ],
            "userID": user_id
        }
        return payload

    @staticmethod
    def post_add_districts_to_user_payload(user_id: int, *data: int or tuple) -> dict:
        payload = {
            "data": [
                *data
            ],
            "userID": user_id
        }
        return payload

    @staticmethod
    def put_update_districts_user_payload(user_id: int, *data: dict) -> dict:
        payload = {
            "userID": user_id,
            "data": [
                *data
            ]
        }
        return payload

    @staticmethod
    def delete_districts_from_user_payload(user_id: int, *districts_ids: int) -> dict:
        payload = {
            "data": [
                *districts_ids
            ],
            "userID": user_id
        }
        return payload
