from src.models.base import StrictBaseModel


class ContactDownloadByIdModel(StrictBaseModel):
    content_type: str | None = None
    body_text: str = ""
    is_vcard: bool = False
