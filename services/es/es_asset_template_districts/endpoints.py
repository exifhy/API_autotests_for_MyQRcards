from config.config import HOST
# import os
#
#
# HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    post_districts_to_asset_templates_endpoint = f'{HOST}/ES/AssetTemplateDistricts'
    delete_districts_from_asset_templates_endpoint = f'{HOST}/ES/AssetTemplateDistricts'

    @staticmethod
    def delete_districts_from_asset_template_by_id_endpoint(template_id: int) -> str:
        return f'{HOST}/ES/AssetTemplateDistricts/{template_id}'
