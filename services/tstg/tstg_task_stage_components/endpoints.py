from config.config import HOST


class Endpoints:

    get_list_task_stage_components_endpoint = f'{HOST}/TSTG/TaskStageComponents/availability'
    post_task_stage_components_endpoint = f'{HOST}/TSTG/TaskStageComponents'
    post_task_stage_components_templates_endpoint = f'{HOST}/TSTG/TaskStageComponents/templates'
