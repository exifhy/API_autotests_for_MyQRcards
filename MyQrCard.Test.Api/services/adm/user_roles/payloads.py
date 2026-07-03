

class Payloads:

    @staticmethod
    def add_roles_to_user_payload(user_id: int, *role_ids: int or tuple) -> list:
        payload = [
            {
                "userID": user_id,
                "roleIDs": [
                    *role_ids
                ]
            }
        ]
        return payload

    @staticmethod
    def delete_users_roles_payload(user_id: int, *roles_ids: int or tuple) -> list:
        payload = [
            {
                "userID": user_id,
                "roleIDs": [
                    *roles_ids
                ]
            }
        ]
        return payload
