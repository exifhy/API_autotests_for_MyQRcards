import os


HOST = "https://dev-api.hubex.ru/fsm" if os.environ["ENVIRON"] == 'qa' else "https://api.hubex.ru/fsm"


class Endpoints:

    account_authentication_by_basic_authorisation_endpoint = f'{HOST}/AUTHN/Accounts/login'

