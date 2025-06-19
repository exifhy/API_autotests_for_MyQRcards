

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
    def post_role_applications_with_list_payload(role_id: int, data_list: list) -> list:
        payload = [
            {
                "roleID": role_id,
                "data": data_list
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
