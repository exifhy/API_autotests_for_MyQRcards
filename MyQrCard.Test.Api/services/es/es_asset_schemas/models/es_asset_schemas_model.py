from typing import Optional, Dict, List
from pydantic import BaseModel, Field, RootModel


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class AssetSchemaBindings(BaseModel):
    id: Optional[int] = None
    assetID: Optional[int] = None
    x: Optional[int] = None
    y: Optional[int] = None


class SuccessGetAssetSchemaModel(BaseModel):
    assets: Optional[List[AssetSchemaBindings]] = None
    schemaID: Optional[int] = None
    assetID: Optional[int] = None
    imageID: Optional[int] = None
    name: Optional[str] = None


class ListAssetSchemasModel(BaseModel):
    schemaID: int
    assetID: int
    imageID: Optional[int] = None
    name: str


class SuccessGetListAssetSchemasModel(RootModel):
    root: Dict[str, ListAssetSchemasModel]


class SuccessUpdateAssetSchemeModel(BaseModel):
    name: str
    id: int


class SuccessCreateAssetSchemeModel(BaseModel):
    name: str
    id: int


class UnbindAssetSchemeFromAssetsModel(BaseModel):
    pointID: int
    taskID: int
    y: int
    x: int


class SuccessUnbindAssetSchemeFromAssetsModel(BaseModel):
    result: List[UnbindAssetSchemeFromAssetsModel]


class ImageSize(BaseModel):
    width: Optional[int] = None
    height: Optional[int] = None


class SuccessAssetSchemaImageModel(BaseModel):
    attachmentID: Optional[int] = None
    fileName: Optional[str] = None
    description: Optional[str] = None
    isUploaded: Optional[bool] = None
    publicUrl: Optional[str] = None
    thumbnailUrl: Optional[str] = None
    isProtected: Optional[bool] = None
    size: Optional[int] = None
    created: Optional[str] = None
    originalSize: Optional[ImageSize] = None


class SuccessUploadFileToAssetSchemeModel(BaseModel):
    attachmentID: int
    md5Hash: Optional[str] = None
    fileName: str
    isProtected: Optional[bool] = None


class SuccessBindAttachmentToAssetSchemeModel(BaseModel):
    schemaID: Optional[int] = None
    assetID: Optional[int] = None
    imageID: Optional[int] = None
    name: Optional[str] = None


class SuccessGetListAssetSchemesAvailableToUser(RootModel):
    root: Dict[str, SuccessBindAttachmentToAssetSchemeModel]


class ListPointsPlacedOnAssetSchemeModel(BaseModel):
    pointID: Optional[int] = None
    taskID: Optional[int] = None
    y: Optional[int] = None
    x: Optional[int] = None


class SuccessGetListPointsPlacedOnAssetSchemeModel(BaseModel):
    result: List[ListPointsPlacedOnAssetSchemeModel]
