

class Payloads:

    @staticmethod
    def post_add_user_template_roles_payload(template_id: int, *role_ids: int) -> list:
        payload = [
            {
                "data": [
                    *role_ids
                ],
                "userTemplateID": template_id
            }
        ]
        return payload

    @staticmethod
    def delete_user_template_roles_payload(template_id: int, *role_ids: int) -> list:
        payload = [
            {
                "data": [
                    *role_ids
                ],
                "userTemplateID": template_id
            }
        ]
        return payload
