from typing import Optional

from src.models.base import StrictBaseModel


class AccountGetModel(StrictBaseModel):
    id: Optional[int] = None
    email: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
