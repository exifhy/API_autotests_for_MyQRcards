from config.config import HOST


class Endpoints:

    put_update_completed_works_endpoint = f'{HOST}/WORK/completedWorks'
    post_add_completed_works_endpoint = f'{HOST}/WORK/completedWorks'
    delete_completed_works_by_list_endpoint = f'{HOST}/WORK/completedWorks'
