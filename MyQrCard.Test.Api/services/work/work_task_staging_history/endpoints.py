from config.config import HOST


class Endpoints:

    add_actual_record_to_history_progress_task_by_stage_endpoint = f'{HOST}/WORK/TaskStagingHistory'
    mass_movement_of_task_by_stage_endpoint = f'{HOST}/WORK/TaskStagingHistory/multiple'
    post_mass_movement_of_task_by_stage_batch_endpoint = f'{HOST}/WORK/TaskStagingHistory/batch'
