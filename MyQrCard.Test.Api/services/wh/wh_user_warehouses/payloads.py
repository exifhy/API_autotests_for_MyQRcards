

class Payloads:

    @staticmethod
    def post_add_multiple_warehouses_to_user_payload(*wh_ids: int or tuple) -> list:
        return [*wh_ids]

    @staticmethod
    def delete_multiple_warehouses_from_user_payload(*wh_ids: int or tuple) -> list:
        return [*wh_ids]

    @staticmethod
    def post_add_multiple_warehouses_to_users_payload(user_ids: list, warehouse_ids_list: list):
        """
        Создает тело запроса в нужном формате.
        :param user_ids: список userID, например [1, 2, 3]
        :param warehouse_ids_list: список списков warehouseID, например [[10], [20, 21], [30]]
        :return: список словарей
        """

        if len(user_ids) != len(warehouse_ids_list):
            raise ValueError("Длина user_ids и warehouse_ids_list должна совпадать")

        payload = []
        for user_id, warehouses in zip(user_ids, warehouse_ids_list):
            payload.append({
                "userID": user_id,
                "warehouseIDs": warehouses
            })

        return payload

    @staticmethod
    def delete_multiple_warehouses_from_users_payload(user_ids: list, warehouse_ids_list: list):
        """
        Создает тело запроса в нужном формате.
        :param user_ids: список userID, например [1, 2, 3]
        :param warehouse_ids_list: список списков warehouseID, например [[10], [20, 21], [30]]
        :return: список словарей
        """

        if len(user_ids) != len(warehouse_ids_list):
            raise ValueError("Длина user_ids и warehouse_ids_list должна совпадать")

        payload = []
        for user_id, warehouses in zip(user_ids, warehouse_ids_list):
            payload.append({
                "userID": user_id,
                "warehouseIDs": warehouses
            })

        return payload
