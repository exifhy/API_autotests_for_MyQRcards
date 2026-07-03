

class Payloads:

    @staticmethod
    def post_user_skills_payload(user_id: int, skill_id: int) -> list:
        payload = [
            {
                "data": [
                    {
                        "skillID": skill_id,
                        "dateFrom": "0001-01-01T00:00:00",
                        "dateTill": "9999-12-31T23:59:59"
                    }
                ],
                "userID": user_id
            }
        ]
        return payload

    @staticmethod
    def put_user_skills_payload(user_id: int, skill_id: int, date_from) -> list:
        payload = [
            {
                "data": [
                    {
                        "skillID": skill_id,
                        "dateFrom": date_from,
                        "dateTill": "9999-12-31T23:59:59"
                    }
                ],
                "userID": user_id
            }
        ]
        return payload

    @staticmethod
    def delete_skills_from_user_payload(user_id: int, *skill_ids: int or tuple) -> list:
        payload = [
            {
                "data": [
                    *skill_ids
                ],
                "userID": user_id
            }
        ]
        return payload
