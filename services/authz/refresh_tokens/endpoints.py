import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    get_refresh_token_with_default_parameters_endpoint = f'{HOST}/AUTHZ/RefreshTokens'
    post_generates_and_returns_refresh_token_endpoint = f'{HOST}/AUTHZ/RefreshTokens'
