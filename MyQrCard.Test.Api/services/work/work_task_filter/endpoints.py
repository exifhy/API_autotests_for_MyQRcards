from config.config import HOST
# import os
#
#
# HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    get_list_task_filter_endpoint = f'{HOST}/WORK/TaskFilter/'
    put_update_task_filter_endpoint = f'{HOST}/WORK/TaskFilter'
