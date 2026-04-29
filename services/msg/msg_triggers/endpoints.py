from config.config import HOST

class Endpoints:

    @staticmethod
    def get_trigger_criticalities_endpoint(trigger_id: int) -> str:
        return f'{HOST}/MSG/Triggers/{trigger_id}/criticalities'

    @staticmethod
    def get_trigger_endpoint(trigger_id: int) -> str:
        return f'{HOST}/MSG/Triggers/{trigger_id}'

    
    @staticmethod
    def delete_trigger_endpoint(trigger_id: int) -> str:
        return f'{HOST}/MSG/Triggers/{trigger_id}'
    
    
    get_triggers_list_endpoint = f'{HOST}/MSG/Triggers'
    post_triggers_endpoint = f'{HOST}/MSG/Triggers'
    put_update_triggers_endpoint = f'{HOST}/MSG/Triggers'
    delete_triggers_endpoint = f'{HOST}/MSG/Triggers'
    
    
    @staticmethod
    def activate_trigger_endpoint(trigger_id: int) -> str:
        return f'{HOST}/MSG/Triggers/{trigger_id}/activate'
    
    
    @staticmethod
    def deactivate_trigger_endpoint(trigger_id: int) -> str:
        return f'{HOST}/MSG/Triggers/{trigger_id}/deactivate'
    
    
    put_activate_triggers_endpoint = f'{HOST}/MSG/Triggers/activate'
    put_deactivate_triggers_endpoint = f'{HOST}/MSG/Triggers/deactivate'
