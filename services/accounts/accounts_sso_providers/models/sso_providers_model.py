from typing import Optional

from src.models.base import StrictBaseModel


class SsoProviderModel(StrictBaseModel):
    providerType: Optional[int] = None
    code: Optional[str] = None
    nameRu: Optional[str] = None
    nameEn: Optional[str] = None
