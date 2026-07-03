

class Payloads:

    @staticmethod
    def post_role_permissions_ui_payload(role_id: int, capability_id: int, *data: int | tuple) -> list:
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
    def post_role_permissions_ui_all_task_payload(role_id: int, capability_id: int) -> list:
        payload = [
            {
                "roleID": role_id,
                "capabilityID": capability_id,
                "data": [
                    -45,-541,-542,-543,-549,-590,-700,-1033,-1034,-1056,-1057,-1090,-1091,-1092,-1148,-1149,-1157,-1158,-1164,-1174,-1177,-1178
                ]
            }
        ]
        return payload

    @staticmethod
    def delete_role_permissions_ui_payload(role_id: int, capability_id: int, *data: int | tuple) -> list:
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
