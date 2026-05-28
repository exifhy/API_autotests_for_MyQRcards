from src.models.base import StrictBaseModel


class SubscriptionContactsDownloadCsvModel(StrictBaseModel):
    content_type: str = ""
    has_bom_utf8: bool = False
    body_text: str = ""
