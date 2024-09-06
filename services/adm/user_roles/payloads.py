from typing import List


class Payloads:

    @staticmethod
    def add_roles_to_user_payload(user_id: int, role_ids: List[int]) -> list:
        payload = [
            {
                "userID": user_id,
                "roleIDs": role_ids
            }
        ]
        return payload
