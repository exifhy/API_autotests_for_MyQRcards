from config.config import HOST

class Endpoints:

    @staticmethod
    def get_recipient_selection_rule_endpoint(rule_id: int) -> str:
        return f'{HOST}/MSG/RecipientSelectionRules/{rule_id}'

    @staticmethod
    def delete_recipient_selection_rule_endpoint(rule_id: int) -> str:
        return f'{HOST}/MSG/RecipientSelectionRules/{rule_id}'

    get_recipient_selection_rules_list_endpoint = f'{HOST}/MSG/RecipientSelectionRules'
    post_recipient_selection_rules_endpoint = f'{HOST}/MSG/RecipientSelectionRules'
    put_update_recipient_selection_rules_endpoint = f'{HOST}/MSG/RecipientSelectionRules'
    delete_recipient_selection_rules_endpoint = f'{HOST}/MSG/RecipientSelectionRules'
    get_recipients_list_endpoint = f'{HOST}/MSG/RecipientSelectionRules/recipients'
