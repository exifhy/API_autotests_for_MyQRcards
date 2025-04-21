from config.config import HOST
# import os
#
#
# HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    put_update_completed_works_endpoint = f'{HOST}/WORK/completedWorks'
    post_add_completed_works_endpoint = f'{HOST}/WORK/completedWorks'
    delete_completed_works_by_list_endpoint = f'{HOST}/WORK/completedWorks'
