import os


HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    add_update_schedules_for_tenant_endpoint = f'{HOST}/PMP/Schedules'

    @staticmethod
    def delete_schedules_endpoint(schedule_id: int) -> str:
        return f'{HOST}/PMP/schedules/{schedule_id}'
