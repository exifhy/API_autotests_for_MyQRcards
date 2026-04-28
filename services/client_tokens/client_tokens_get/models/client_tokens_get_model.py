from typing import Optional

from src.models.base import StrictBaseModel


class ClientTokensGetModel(StrictBaseModel):
    clientID: Optional[str] = None
    pushToken: Optional[str] = None
    created: Optional[str] = None

