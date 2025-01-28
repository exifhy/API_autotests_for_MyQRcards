

class Payloads:

    @staticmethod
    def post_update_attributes_to_asset_template_payload(
            template_id: int,
            *attribute_data: dict
    ) -> list:
        payload = [
            {
                "assetTemplateID": template_id,
                "data": [*attribute_data]
            }
        ]
        return payload

    @staticmethod
    def post_delete_attributes_from_asset_template_payload(
            template_id: int,
    ) -> list:
        payload = [
            {
                "assetTemplateID": template_id,
                "data": []
            }
        ]
        return payload
