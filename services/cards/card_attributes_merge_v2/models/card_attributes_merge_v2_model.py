from typing import Optional

from src.models.base import StrictBaseModel


class CardAttributeMergeV2ItemModel(StrictBaseModel):
    """One entry of the PUT /attributes/V2 response — a flat list of created/updated
    nodes (not a tree; the tree shape is only returned by GET)."""

    accountID: Optional[int] = None
    cardID: Optional[int] = None
    attributeID: Optional[int] = None
    id: Optional[int] = None
    cardAttributeNodeID: Optional[int] = None
