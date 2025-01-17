

class Payloads:

    @staticmethod
    def post_add_warehouse_payload(name: str, erp_name: str, default: bool) -> list:
        payload = [
            {
                "name": name,
                "erpID": erp_name,
                "isDefault": default
            }
        ]
        return payload

    @staticmethod
    def delete_warehouses_by_list(*wh_ids: tuple) -> list:
        return [*wh_ids]
