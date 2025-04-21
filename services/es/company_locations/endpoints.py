from config.config import HOST
# import os
#
#
# HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    post_add_company_locations_endpoint = f'{HOST}/ES/CompanyLocations'
    get_list_company_locations_endpoint = f'{HOST}/ES/CompanyLocations'
    put_update_company_location_endpoint = f'{HOST}/ES/CompanyLocations'
    delete_locations_from_company_endpoint = f'{HOST}/ES/CompanyLocations'
