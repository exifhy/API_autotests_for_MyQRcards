import os


HOST = "https://dev-api.hubex.ru/fsm" if os.environ["ENVIRON"] == 'qa' else "https://api.hubex.ru/fsm"


class Endpoints:

    authorisation_endpoint = f'{HOST}/AUTHZ/accounts/authorize'
