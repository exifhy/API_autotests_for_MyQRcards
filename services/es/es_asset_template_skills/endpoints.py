import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    post_add_skills_to_asset_templates_endpoint = f'{HOST}/ES/AssetTemplateSkills'
    delete_skills_from_asset_templates_endpoint = f'{HOST}/ES/AssetTemplateSkills'

    @staticmethod
    def delete_skills_from_asset_template_by_id_endpoint(template_id: int) -> str:
        return f'{HOST}/ES/AssetTemplateSkills/{template_id}'
