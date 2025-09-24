

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

    @staticmethod
    def delete_list_users_from_warehouse_by_id_payload(*users_ids: int) -> list:
        return [*users_ids]

    @staticmethod
    def post_add_many_users_to_warehouse_by_list(*user_ids: tuple) -> list:
        return [*user_ids]

    @staticmethod
    def delete_many_users_from_warehouse_by_list(*user_ids: tuple) -> list:
        return [*user_ids]

    @staticmethod
    def post_add_all_users_to_warehouse_by_list_payload(wh_ids: int) -> list:
        payload = [
            {
                "warehouseID": wh_ids,
                "isRelatedToAnyUser": True
            }
        ]
        return payload

    @staticmethod
    def post_add_empty_list_users_to_warehouse_by_list_payload(wh_ids: int) -> list:
        payload = [
            {
                "warehouseID": wh_ids,
                "userIDs": []
            }
        ]
        return payload

    @staticmethod
    def delete_empty_list_users_from_valid_warehouse_by_list_payload(wh_ids: int) -> list:
        payload = [
            {
                "warehouseID": wh_ids,
                "userIDs": []
            }
        ]
        return payload

    @staticmethod
    def post_add_null_user_to_warehouse_by_list_payload(wh_ids: int) -> list:
        payload = [
            {
                "warehouseID": wh_ids,
                "userIDs": None
            }
        ]
        return payload

    @staticmethod
    def post_add_all_users_with_user_id_to_warehouse_by_list_payload(wh_ids: int, user_id: int) -> list:
        payload = [
            {
                "warehouseID": wh_ids,
                "userIDs": [user_id],
                "isRelatedToAnyUser": True
            }
        ]
        return payload

    @staticmethod
    def delete_valid_users_from_warehouse_null_by_list_payload(user_id: int) -> list:
        payload = [
            {
                "warehouseID": None,
                "userIDs": [user_id]
            }
        ]
        return payload

    @staticmethod
    def delete_user_null_from_valid_warehouse_by_list_payload(wh_id: int) -> list:
        payload = [
            {
                "warehouseID": wh_id,
                "userIDs": None
            }
        ]
        return payload

    @staticmethod
    def delete_all_users_from_warehouses_payload(wh_ids: int, *user_ids: int or tuple) -> list:
        payload = [
            {
                "warehouseID": wh_ids,
                "userIDs": [*user_ids],
                "isRelatedToAnyUser": True
            }
        ]
        return payload

    @staticmethod
    def post_add_multiple_users_to_warehouses_payload(wh_ids: list, users_ids_list: list):
        """
        Создает тело запроса в нужном формате.
        :param wh_ids: Список warehouseID, например [1, 2, 3].
        :param users_ids_list: Список списков userIDs, например [[10], [20, 21], [30]].
        :return: Список словарей.
        """

        if len(wh_ids) != len(users_ids_list):
            raise ValueError("Длина wh_ids и users_ids_list должна совпадать")

        payload = []
        for wh_id, users in zip(wh_ids, users_ids_list):
            payload.append({
                "warehouseID": wh_id,
                "userIDs": users
            })

        return payload

    @staticmethod
    def delete_multiple_users_from_warehouses_payload(wh_ids: list, users_ids_list: list):
        """
        Создает тело запроса в нужном формате.
        :param wh_ids: Список warehouseID, например [1, 2, 3].
        :param users_ids_list: Список списков userIDs, например [[10], [20, 21], [30]].
        :return: Список словарей.
        """

        if len(wh_ids) != len(users_ids_list):
            raise ValueError("Длина wh_ids и users_ids_list должна совпадать")

        payload = []
        for wh_id, users in zip(wh_ids, users_ids_list):
            payload.append({
                "warehouseID": wh_id,
                "userIDs": users
            })

        return payload
