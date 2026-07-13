

class Payloads:

    @staticmethod
    def post_role_permissions_ext_payload(role_id: int, *data: int | tuple) -> list:
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
    def post_role_permissions_ext_all_task_payload(role_id: int) -> list:
        payload = [
            {
                "roleID": role_id,
                "data": [
                    5, 7, 8, 9, 11, 12, 14, 28, 33, 34, 35, 36, 37, 42, 46, 48, 49, 52, 55
                ]
            }
        ]
        return payload

    @staticmethod
    def delete_role_permissions_ext_payload(role_id: int, *data: int | tuple) -> list:
        payload = [
            {
                "roleID": role_id,
                "data": [
                    *data
                ]
            }
        ]
        return payload
