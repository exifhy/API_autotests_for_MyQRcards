from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, RootModel,  ConfigDict


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class AddTaskTypeRouteModel(StrictBaseModel):
    results: List[int]
