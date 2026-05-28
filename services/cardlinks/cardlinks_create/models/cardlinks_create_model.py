from typing import Optional

from src.models.base import StrictBaseModel


class CardLinksCreateModel(StrictBaseModel):
    id: Optional[str] = None
