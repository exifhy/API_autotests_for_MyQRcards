from config.config import HOST
# import os
#
#
# HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    post_add_user_task_favourites_endpoint = f'{HOST}/WORK/UserTaskFavourites'
    delete_user_task_favourites_by_list_endpoint = f'{HOST}/WORK/UserTaskFavourites'
