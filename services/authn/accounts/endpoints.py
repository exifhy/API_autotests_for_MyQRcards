import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    account_authentication_by_basic_authorisation_endpoint = f'{HOST}/AUTHN/accounts/login'

