from pydantic import BaseModel, ConfigDict


class AccountActionCreateModel(BaseModel):
    model_config = ConfigDict(extra="allow")
