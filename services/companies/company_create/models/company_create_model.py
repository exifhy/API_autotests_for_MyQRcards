from typing import Optional

from src.models.base import StrictBaseModel


class CompanyCreateModel(StrictBaseModel):
    id: Optional[int] = None

