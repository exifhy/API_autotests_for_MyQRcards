from typing import Optional

from pydantic import BaseModel, ConfigDict


class CardLinkByIdModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: Optional[int] = None
    cardID: Optional[int] = None
    accountID: Optional[int] = None
    name: Optional[str] = None
    customCardLinkUrl: Optional[str] = None
    isDefault: Optional[bool] = None
