

class Payloads:

    @staticmethod
    def post_add_tenant_members_payload(*data: dict or tuple) -> list:
        return [*data]

    @staticmethod
    def put_update_tenant_members_payload(*data: dict or tuple) -> list:
        return [*data]

    @staticmethod
    def delete_tenant_members_by_list_payload(*data: int or tuple) -> list:
        return [*data]
