from config.config import HOST


class Endpoints:
    merge_accounts_card_attributes_v2_endpoint = f"{HOST}/Accounts/{{account_id}}/cards/{{card_id}}/attributes/V2"
