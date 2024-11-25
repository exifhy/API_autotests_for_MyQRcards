import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    post_skills_to_assets_endpoint = f'{HOST}/ES/assetSkills'
    delete_skills_from_assets_endpoint = f'{HOST}/ES/assetSkills'
