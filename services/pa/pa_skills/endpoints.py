from config.config import HOST
# import os
#
#
# HOST = os.getenv('URL_DEV_HUBEX') if os.environ["ENVIRON"] == 'qa' else os.getenv('URL_PROD_HUBEX')


class Endpoints:

    get_list_skills_for_tenant_endpoint = f'{HOST}/PA/skills'
    put_update_skills_for_tenant_endpoint = f'{HOST}/PA/skills'
    post_add_skills_for_tenant_endpoint = f'{HOST}/PA/skills'
    delete_skills_endpoint = f'{HOST}/PA/skills'

    @staticmethod
    def get_skill_by_id(skill_id: int) -> str:
        return f'{HOST}/PA/skills/{skill_id}'

    @staticmethod
    def delete_skill_by_id(skill_id: int) -> str:
        return f'{HOST}/PA/skills/{skill_id}'
