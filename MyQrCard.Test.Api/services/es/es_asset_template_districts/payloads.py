

class Payloads:

    @staticmethod
    def post_districts_to_asset_templates_payload(template_id: int, *district_id: int) -> list:
        payload = [
            {
                "assetTemplateID": template_id,
                "data": [
                    *district_id
                ]
            }
        ]
        return payload

    @staticmethod
    def delete_districts_from_asset_templates_payload(template_id: int, *district_id: int) -> list:
        payload = [
            {
                "assetTemplateID": template_id,
                "data": [
                    *district_id
                ]
            }
        ]
        return payload

    @staticmethod
    def delete_districts_from_asset_template_by_id_payload(*district_id: int) -> list:
        return [*district_id]
