import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    post_task_template_excluded_assets_endpoint = f'{HOST}/WORK/TaskTemplateExcludedAssets'
    delete_task_template_excluded_assets_endpoint = f'{HOST}/WORK/TaskTemplateExcludedAssets'
