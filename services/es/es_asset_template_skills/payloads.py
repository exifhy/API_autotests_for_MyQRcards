

class Payloads:

    @staticmethod
    def post_add_skills_to_asset_templates_payload(template_id: int, *skills: dict) -> list:
        payload = [
            {
                "assetTemplateID": template_id,
                "data": [*skills]
            }
        ]
        return payload

    @staticmethod
    def delete_skills_from_asset_templates_payload(template_id: int, *skill_ids: int) -> list:
        payload = [
            {
                "assetTemplateID": template_id,
                "data": [*skill_ids]
            }
        ]
        return payload

    @staticmethod
    def delete_skills_from_asset_template_by_id_payload(*skill_ids: int) -> list:
        return [*skill_ids]

