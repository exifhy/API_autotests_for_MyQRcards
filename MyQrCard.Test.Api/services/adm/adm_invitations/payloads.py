

class Payloads:

    @staticmethod
    def post_add_invitations_payload(*data) -> list:
        return [*data]

    @staticmethod
    def put_update_invitations_payload(*data) -> list:
        return [*data]

    @staticmethod
    def delete_invitations_by_list_payload(*data: str or tuple) -> list:
        return [*data]
