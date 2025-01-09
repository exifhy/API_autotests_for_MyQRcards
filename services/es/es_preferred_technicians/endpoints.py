import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    get_preferred_technicians_endpoint = f'{HOST}/ES/PreferredTechnicians'
    post_preferred_technicians_endpoint = f'{HOST}/ES/PreferredTechnicians'
