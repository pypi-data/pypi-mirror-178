from datetime import datetime, timezone
from pydantic import BaseModel, Extra, Field, validator

from gww_service.schemas.geometry_types import PatchedFeature


class ImageFeatureProperties(BaseModel, extra=Extra.allow):
    t: datetime = Field(
        ...,
        example="2022-01-01T00:00:00.000Z"
    )

    @validator("t")
    def timezone_none_to_utc(cls, v: datetime):
        if not v.tzinfo:
            v = v.replace(tzinfo=timezone.utc)
        return v


class ImageFeature(PatchedFeature):

    properties: ImageFeatureProperties


class UrlFormat(BaseModel):
    url: str = Field(
        ...,
        example=("https://earthengine.googleapis.com/v1alpha/projects/earthengine-legacy/maps/"
            "b65484d606efd58300d61b53e11ff185-a831cc14ae14107768d8069300106e4b/tiles/{z}/{x}/{y}")
    )
