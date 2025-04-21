from config.config import HOST
# import os
#
#
# HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    post_update_attributes_to_asset_template_endpoint = f'{HOST}/ES/assetTemplateAttributes'
