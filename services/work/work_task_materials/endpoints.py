import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    put_task_materials_endpoint = f'{HOST}/WORK/TaskMaterials'
    post_task_materials_endpoint = f'{HOST}/WORK/TaskMaterials'
    delete_task_materials_endpoint = f'{HOST}/WORK/TaskMaterials'
    put_task_materials_take_on_endpoint = f'{HOST}/WORK/TaskMaterials/takeOn'
    put_task_materials_take_off_endpoint = f'{HOST}/WORK/TaskMaterials/takeOff'
