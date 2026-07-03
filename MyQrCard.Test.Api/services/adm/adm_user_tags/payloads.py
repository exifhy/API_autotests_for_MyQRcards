

class Payloads:

    @staticmethod
    def post_add_user_tags_payload(tags: str, user_id: int) -> list:
        payload = [
            {
                "tags": [
                    tags
                ],
                "userID": user_id
            }
        ]
        return payload

    @staticmethod
    def delete_user_tags_payload(user_id: int, *tags: str or tuple) -> list:
        payload = [
            {
                "tags": [
                    *tags
                ],
                "userID": user_id
            }
        ]
        return payload
