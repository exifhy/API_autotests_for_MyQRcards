from typing import Any

from pydantic import BaseModel, ConfigDict


class AccountActionItemModel(BaseModel):
    model_config = ConfigDict(extra="allow")


class AccountActionsGetModel(BaseModel):
    items: list[AccountActionItemModel]
    raw: list[dict[str, Any]]

    @property
    def access_jwt(self) -> str | None:
        for item in self.items:
            extras = item.model_extra or {}
            for key in ("accessJWT", "accessJwt", "AccessJWT", "accessToken", "AccessToken"):
                val = extras.get(key)
                if val:
                    return str(val)
        return None
