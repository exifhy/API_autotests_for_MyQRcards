

class Payloads:

    @staticmethod
    def post_add_warehouse_payload(name: str, erp_name: str) -> list:
        payload = [
            {
                "name": name,
                "erpID": erp_name
            }
        ]
        return payload

    @staticmethod
    def post_add_warehouse_with_different_fields_payload(*data: dict) -> list:
        return [*data]

    @staticmethod
    def put_update_warehouse_payload(*data: dict) -> list:
        return [*data]

    @staticmethod
    def put_restore_warehouses_by_list_payload(*wh_ids: int) -> list:
        return [*wh_ids]

    @staticmethod
    def delete_warehouses_by_list(*wh_ids: tuple) -> list:
        return [*wh_ids]
