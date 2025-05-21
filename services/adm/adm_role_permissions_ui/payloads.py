

class Payloads:

    @staticmethod
    def post_role_permissions_ui_payload(role_id: int, capability_id: int, *data: int or tuple) -> list:
        payload = [
            {
                "roleID": role_id,
                "capabilityID": capability_id,
                "data": [
                    *data
                ]
            }
        ]
        return payload

    @staticmethod
    def delete_role_permissions_ui_payload(role_id: int, capability_id: int, *data: int or tuple) -> list:
        payload = [
            {
                "roleID": role_id,
                "capabilityID": capability_id,
                "data": [
                    *data
                ]
            }
        ]
        return payload
