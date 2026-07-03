from config.config import HOST


class Endpoints:

    @staticmethod
    def get_operation_types_by_id_endpoint(type_id: int) -> str:
        return f'{HOST}/WH/OperationTypes/{type_id}'

    @staticmethod
    def delete_operation_types_by_id_endpoint(type_id: int) -> str:
        return f'{HOST}/WH/OperationTypes/{type_id}'
    
    get_list_operation_types_endpoint = f'{HOST}/WH/OperationTypes'
    post_operation_types_endpoint = f'{HOST}/WH/OperationTypes'
    put_operation_types_endpoint = f'{HOST}/WH/OperationTypes'
    delete_operation_types_endpoint = f'{HOST}/WH/OperationTypes'
