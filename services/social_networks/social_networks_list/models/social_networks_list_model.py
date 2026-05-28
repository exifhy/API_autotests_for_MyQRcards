from typing import Optional

from src.models.base import StrictBaseModel


class SocialNetworkItemModel(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    nameEn: Optional[str] = None


class SocialNetworksListModel(StrictBaseModel):
    items: list[SocialNetworkItemModel]

