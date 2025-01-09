import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    post_add_task_attributes_endpoint = f'{HOST}/WORK/taskAttributes'
    get_list_task_attributes_endpoint = f'{HOST}/WORK/taskAttributes'
