from typing import Optional

from src.models.base import StrictBaseModel


class ContactCreateWebModel(StrictBaseModel):
    id: Optional[int] = None
