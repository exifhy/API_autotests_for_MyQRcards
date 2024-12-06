import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    post_add_work_types_to_asset_templates_endpoint = f'{HOST}/ES/AssetTemplateWorkTypes'
    delete_work_types_from_asset_templates_endpoint = f'{HOST}/ES/AssetTemplateWorkTypes'

    @staticmethod
    def delete_work_types_from_asset_template_by_id_endpoint(template_id: int) -> str:
        return f'{HOST}/ES/AssetTemplateWorkTypes/{template_id}'
