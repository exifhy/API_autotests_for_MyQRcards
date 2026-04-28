from src.models.base import StrictBaseModel


class ContactsDownloadCsvModel(StrictBaseModel):
    content_type: str | None = None
    has_bom_utf8: bool = False
    body_text: str = ""
