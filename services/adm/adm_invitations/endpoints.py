from config.config import HOST


class Endpoints:

    @staticmethod
    def get_invitation_by_id_endpoint(inv_id: str) -> str:
        return f'{HOST}/ADM/invitations/{inv_id}'

    @staticmethod
    def delete_invitation_by_id_endpoint(inv_id: str) -> str:
        return f'{HOST}/ADM/invitations/{inv_id}'

    @staticmethod
    def get_short_invitation_by_id_endpoint(inv_id: str) -> str:
        return f'{HOST}/ADM/invitations/{inv_id}/short'

    get_list_invitations_endpoint = f'{HOST}/ADM/invitations'
    post_add_invitations_endpoint = f'{HOST}/ADM/invitations'
    put_update_invitations_endpoint = f'{HOST}/ADM/invitations'
    delete_invitations_by_list_endpoint = f'{HOST}/ADM/invitations'
