from config.config import HOST
# import os
#
#
# HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    post_user_api_token_generation_endpoint = f'{HOST}/AUTHZ/ServiceTokens'
    delete_user_api_token_endpoint = f'{HOST}/AUTHZ/ServiceTokens'
