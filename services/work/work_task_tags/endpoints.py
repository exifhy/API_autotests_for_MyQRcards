from config.config import HOST
# import os
#
#
# HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    post_task_tags_endpoint = f'{HOST}/WORK/TaskTags'
    delete_task_tags_endpoint = f'{HOST}/WORK/TaskTags'
