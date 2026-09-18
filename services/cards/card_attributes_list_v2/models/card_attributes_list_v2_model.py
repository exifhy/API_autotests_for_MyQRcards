from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class CardAttributeNodeV2Model(BaseModel):
    """A single node of the /attributes/V2 tree. `extra="allow"` — same as v1
    card attribute models, the shape varies a lot per attribute type."""

    model_config = ConfigDict(extra="allow")

    cardAttributeNodeID: Optional[int] = None
    # Absent (not null) on root nodes — only present on non-root nodes.
    parentCardAttributeNodeID: Optional[int] = None
    children: list["CardAttributeNodeV2Model"] = []
    accountID: Optional[int] = None
    cardID: Optional[int] = None
    sortOrder: Optional[int] = None
    isEnabled: Optional[bool] = None
    values: Optional[list] = None


CardAttributeNodeV2Model.model_rebuild()
