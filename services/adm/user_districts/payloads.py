

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
