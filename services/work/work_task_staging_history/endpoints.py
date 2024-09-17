import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    add_actual_record_to_history_progress_task_by_stage_endpoint = f'{HOST}/WORK/TaskStagingHistory'
    mass_movement_of_task_by_stage_endpoint = f'{HOST}/WORK/TaskStagingHistory/multiple'

