

class Payloads:

    @staticmethod
    def post_role_applications_payload(role_id: int, *data: int or tuple) -> list:
        payload = [
            {
                "roleID": role_id,
                "data": [
                    *data
                ]
            }
        ]
        return payload

    @staticmethod
    def delete_role_applications_payload(role_id: int, *data: int or tuple) -> list:
        payload = [
            {
                "roleID": role_id,
                "data": [
                    *data
                ]
            }
        ]
        return payload
