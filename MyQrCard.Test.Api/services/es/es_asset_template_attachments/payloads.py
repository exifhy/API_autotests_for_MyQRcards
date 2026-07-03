

class Payloads:

    @staticmethod
    def post_bind_attachments_to_asset_template_payload(template_id: int, *attachment_id: int) -> list:
        payload = [
            {
                "assetTemplateID": template_id,
                "data": [*attachment_id]
            }
        ]
        return payload

    @staticmethod
    def delete_attachments_from_asset_template_payload(template_id: int, *attachment_id: int) -> list:
        payload = [
            {
                "assetTemplateID": template_id,
                "data": [*attachment_id]
            }
        ]
        return payload
