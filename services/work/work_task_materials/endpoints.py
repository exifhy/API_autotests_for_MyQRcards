from config.config import HOST


class Endpoints:

    put_task_materials_endpoint = f'{HOST}/WORK/TaskMaterials'
    post_task_materials_endpoint = f'{HOST}/WORK/TaskMaterials'
    delete_task_materials_endpoint = f'{HOST}/WORK/TaskMaterials'
    put_task_materials_take_on_endpoint = f'{HOST}/WORK/TaskMaterials/takeOn'
    put_task_materials_take_off_endpoint = f'{HOST}/WORK/TaskMaterials/takeOff'
