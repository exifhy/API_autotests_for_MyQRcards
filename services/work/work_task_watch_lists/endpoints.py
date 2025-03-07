import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    post_add_task_watch_lists_endpoint = f'{HOST}/WORK/TaskWatchLists'
    delete_task_watch_lists_endpoint = f'{HOST}/WORK/TaskWatchLists'
