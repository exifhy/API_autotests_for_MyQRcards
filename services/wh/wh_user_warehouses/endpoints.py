from config.config import HOST


class Endpoints:

    @staticmethod
    def get_list_user_warehouses_endpoint(user_id: int) -> str:
        return f'{HOST}/WH/UserWarehouses/{user_id}'

    @staticmethod
    def post_add_multiple_warehouses_to_user_endpoint(user_id: int) -> str:
        return f'{HOST}/WH/UserWarehouses/{user_id}'

    @staticmethod
    def delete_multiple_warehouses_from_user_endpoint(user_id: int) -> str:
        return f'{HOST}/WH/UserWarehouses/{user_id}'

    post_add_multiple_warehouses_to_users_endpoint = f'{HOST}/WH/UserWarehouses'
    delete_multiple_warehouses_from_users_endpoint = f'{HOST}/WH/UserWarehouses'
