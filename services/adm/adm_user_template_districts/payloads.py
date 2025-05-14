

class Payloads:

    @staticmethod
    def post_add_user_template_districts_payload(template_id: int, *districts_ids: int) -> list:
        payload = [
            {
                "data": [
                    *districts_ids
                ],
                "userTemplateID": template_id
            }
        ]
        return payload

    @staticmethod
    def delete_user_template_districts_payload(template_id: int, *districts_ids: int) -> list:
        payload = [
            {
                "data": [
                    *districts_ids
                ],
                "userTemplateID": template_id
            }
        ]
        return payload
