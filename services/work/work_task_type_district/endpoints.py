import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    put_update_task_type_district_endpoint = f'{HOST}/WORK//TaskTypeDistrict'
