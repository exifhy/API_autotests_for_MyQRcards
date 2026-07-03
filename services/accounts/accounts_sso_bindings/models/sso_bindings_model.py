from typing import Optional

from src.models.base import StrictBaseModel


class SsoBindingModel(StrictBaseModel):
    providerType: Optional[int] = None
    providerCode: Optional[str] = None
    providerNameRu: Optional[str] = None
    providerNameEn: Optional[str] = None
    ssoid: Optional[str] = None
    isVerified: Optional[bool] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    avatarUrl: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
