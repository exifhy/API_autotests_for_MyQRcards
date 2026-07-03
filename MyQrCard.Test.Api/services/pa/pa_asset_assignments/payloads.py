

class Payloads:

    @staticmethod
    def post_add_asset_assignments_payload(*data: dict or tuple) -> list:
        return [*data]

    @staticmethod
    def delete_users_asset_assignments_payload(*data: dict or tuple) -> list:
        return [*data]
