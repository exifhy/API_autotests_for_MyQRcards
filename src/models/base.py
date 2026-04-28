from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class StrictBaseModel(BaseModel):
    """Base model that rejects unknown fields from API responses.
    If the API returns a field not declared in the model — the test fails immediately,
    forcing you to keep models up to date with the actual API contract.
    """
    model_config = ConfigDict(extra="forbid")


class ErrorItemModel(StrictBaseModel):
    code: str
    message: str
    traceIdentifier: Optional[str] = None
    arguments: Optional[dict[str, Any]] = None


class ErrorModel(BaseModel):
    list_model: list[ErrorItemModel]

    @classmethod
    def from_response(cls, response) -> "ErrorModel":
        data = response.json()
        if isinstance(data, list):
            return cls(list_model=[ErrorItemModel(**item) for item in data])
        if isinstance(data, dict) and "errors" in data:
            return cls(list_model=[ErrorItemModel(**item) for item in data["errors"]])
        return cls(list_model=[ErrorItemModel(**data)])
