

class Payloads:

    @staticmethod
    def post_add_work_types_to_asset_templates_payload(template_id: int, *work_type_id: int) -> list:
        payload = [
            {
                "assetTemplateID": template_id,
                "data": [
                    *work_type_id
                ]
            }
        ]
        return payload

    @staticmethod
    def delete_work_types_from_asset_templates_payload(template_id: int, *work_type_id: int) -> list:
        payload = [
            {
                "assetTemplateID": template_id,
                "data": [
                    *work_type_id
                ]
            }
        ]
        return payload

    @staticmethod
    def delete_work_types_from_asset_template_by_id(*work_type_id) -> list:
        return [*work_type_id]
