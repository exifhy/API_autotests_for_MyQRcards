from typing import Optional

from src.models.base import StrictBaseModel


class GoogleWalletResultModel(StrictBaseModel):
    jwt: Optional[str] = None
    saveUrl: Optional[str] = None
