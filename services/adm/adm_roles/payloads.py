

class Payloads:

    @staticmethod
    def post_add_roles_payload(*data: dict | tuple) -> list:
        return [*data]

    @staticmethod
    def post_copy_roles_payload(*data: dict | tuple) -> list:
        return [*data]

    @staticmethod
    def put_update_roles_payload(*data: dict | tuple) -> list:
        return [*data]

    @staticmethod
    def delete_roles_by_list_payload(*data: int | tuple) -> list:
        return [*data]

    @staticmethod
    def post_add_packages_to_roles_payload(package_id: str, package_version: str, status: bool) -> list:
        payload = [
            {
            "packageID": package_id,
            "packageVersion": package_version,
            "isEnabled": status
            }
        ]
        return payload

    @staticmethod
    def delete_packages_from_roles_by_list_payload(*data: int | tuple) -> list:
        return [*data]

    @staticmethod
    def put_activate_packages_roles_by_list_payload(*data: int | tuple) -> list:
        return [*data]

    @staticmethod
    def put_deactivate_packages_roles_by_list_payload(*data: int | tuple) -> list:
        return [*data]
