from config.config import HOST


class Endpoints:
    delete_attachment_by_id_endpoint = f"{HOST}/Attachments/{{attachment_id}}"
