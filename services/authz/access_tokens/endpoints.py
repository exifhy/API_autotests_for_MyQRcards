import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    updates_resource_access_token_endpoint = f'{HOST}/AUTHZ/AccessTokens'
