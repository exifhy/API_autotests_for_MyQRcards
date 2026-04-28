from typing import Optional

from src.models.base import StrictBaseModel


class ContactCreateAppModel(StrictBaseModel):
    id: Optional[int] = None
