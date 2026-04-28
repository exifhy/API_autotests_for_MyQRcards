from typing import Optional

from src.models.base import StrictBaseModel


class VirtualBackgroundAttachmentModel(StrictBaseModel):
    fileName: Optional[str] = None
    id: Optional[int] = None
    url: Optional[str] = None


class VirtualBackgroundItemModel(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    attachment: Optional[VirtualBackgroundAttachmentModel] = None


class VirtualBackgroundsModel(StrictBaseModel):
    items: list[VirtualBackgroundItemModel]

