from config.config import HOST
# import os
#
#
# HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    authorization_endpoint = f'{HOST}/AUTHZ/accounts/authorize'
    authorization_api_user_token_endpoint = f'{HOST}/AUTHZ/AccessTokens'
