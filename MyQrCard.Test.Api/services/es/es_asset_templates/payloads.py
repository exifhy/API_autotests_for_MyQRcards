

class Payloads:

    @staticmethod
    def post_add_asset_templates_endpoint(*params: dict) -> list:
        return [*params]

    @staticmethod
    def put_update_asset_templates_endpoint(*params: dict) -> list:
        return [*params]

    @staticmethod
    def delete_asset_templates_by_lyst_endpoint(*templates_id: dict) -> list:
        return [*templates_id]

    @staticmethod
    def delete_avatar_from_asset_templates_by_lyst_endpoint(*templates_id: dict) -> list:
        return [*templates_id]
