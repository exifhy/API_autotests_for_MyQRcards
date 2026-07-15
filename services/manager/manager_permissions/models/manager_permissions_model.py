from pydantic import BaseModel, ConfigDict


class ManagerPermissionsModel(BaseModel):
    """REQUIREMENT 29760. Response shape not yet confirmed against a real manager
    account — extra="allow" until verified, tighten to StrictBaseModel afterwards.
    """
    model_config = ConfigDict(extra="allow")
