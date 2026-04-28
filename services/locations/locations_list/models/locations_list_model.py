from typing import Optional

from src.models.base import StrictBaseModel


class LocationListItemModel(StrictBaseModel):
    country: Optional[str] = None
    postalCode: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class LocationsListModel(StrictBaseModel):
    items: dict[str, LocationListItemModel]
