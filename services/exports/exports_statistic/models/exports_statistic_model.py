from src.models.base import StrictBaseModel


class ExportsStatisticModel(StrictBaseModel):
    content_type: str | None = None
    content_disposition: str | None = None
    is_xlsx: bool = False
