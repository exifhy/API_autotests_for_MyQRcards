from typing import Optional

from src.models.base import StrictBaseModel


class CardAttachmentSortOrderItemModel(StrictBaseModel):
    attachmentID: Optional[int] = None
    sortOrder: Optional[int] = None


class CardAttachmentsSortOrderResponseModel(StrictBaseModel):
    attachmentSortOrder: list[CardAttachmentSortOrderItemModel] = []
