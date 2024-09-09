import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    export_list_tasks_extended_endpoint = f'{HOST}/EXPORT/tasks/extended/includes'
