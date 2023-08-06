import ee
import fastapi

from gww_service.earthengine import get_image_for_geometry_t
from gww_service.schemas.images import ImageFeature, UrlFormat

router = fastapi.APIRouter(
    prefix="/images",
    tags=["images"]
)

@router.post("/satellite/t", response_model=UrlFormat)
def get_url_format_for_geometry_t(feature: ImageFeature):
    geometry = ee.Geometry(feature.geometry.dict())
    t = ee.Date(feature.properties.t.timestamp() * 1000)

    # Look 300m out of reservoir before we start to fade out
    image = get_image_for_geometry_t(geometry.buffer(300), t)
    map_id = image.getMapId({})
    res = {"url": map_id["tile_fetcher"]._url_format}
    return res
