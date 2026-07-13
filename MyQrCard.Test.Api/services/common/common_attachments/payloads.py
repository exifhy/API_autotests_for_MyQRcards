

class Payloads:

    @staticmethod
    def delete_attachments_by_list_payload(*attach_ids: int or tuple) -> list:
        return [*attach_ids]
