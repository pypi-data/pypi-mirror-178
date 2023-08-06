from logging import getLogger
from logging.config import dictConfig
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from geoalchemy2 import WKBElement
from geojson_pydantic import MultiPolygon
from pydantic import BaseModel, Field, root_validator, validator
from pydantic.utils import GetterDict
from shapely import wkb
from shapely import geometry

from gww_service.config import LogConfig
from gww_service.schemas.geometry_types import PatchedFeature
from gww_service.schemas.time_series import TimeSeriesUnits

if TYPE_CHECKING:
    from gww_service import models

dictConfig(LogConfig().dict())
logger = getLogger("gww-service")

class ReservoirProperties(BaseModel):
    class Config:
        orm_mode = True
    
    name: Optional[str] = None
    name_en: Optional[str] = None
    grand_id: Optional[int] = None
    source_name: Optional[str] = None
    source_id: Optional[int] = None

class ReservoirBase(PatchedFeature):

    type: str = 'Feature'
    geometry: MultiPolygon = Field(...,
        example={
            "coordinates": [
                [
                    [
                        [-84.09437, 30.86229],
                        [-84.094708, 30.862161],
                        [-84.094931, 30.862241],
                        [-84.094927, 30.862714],
                        [-84.094766, 30.862772],
                        [-84.094753, 30.86233],
                        [-84.09437, 30.86229]
                    ]
                ],
                [
                    [
                        [-84.09437, 30.86229],
                        [-84.09437, 30.862607],
                        [-84.094749, 30.862803],
                        [-84.094316, 30.862856],
                        [-84.094191, 30.862696],
                        [-84.094124, 30.862522],
                        [-84.09437, 30.86229]
                    ]
                ]
            ],
            "type": "MultiPolygon"
        }
    )
    properties: ReservoirProperties
    
    @validator("geometry", pre=True)
    def wkb_to_multipolygon(cls, v) -> MultiPolygon:
        """
        validator to translate wkb coordinates obtained from postgis to multipolygon coords
        """ 
        if isinstance(v, WKBElement):
            shp: geometry.MultiPolygon = wkb.loads(bytes(v.data))
            return MultiPolygon(coordinates=geometry.mapping(shp)["coordinates"])
        else:
            return v

class ReservoirCreate(ReservoirBase):
    pass

class Reservoir(ReservoirBase):
    id: int
    class Config:
        orm_mode = True
    
    @classmethod
    def from_sqlachemy_model(cls, model: "models.Reservoir") -> "Reservoir":
        props: ReservoirProperties = ReservoirProperties.from_orm(model)
        return cls(
            id=model.reservoir_id,
            geometry=model.geometry,  # will automatically get converted
            properties=props
        )
    
    @root_validator(pre=True)
    def model_to_schema(cls: "Reservoir", values: GetterDict) -> GetterDict:
        new_values: Dict[str, Any] = {}
        
        if "properties" not in values.keys():
            properties: ReservoirProperties = ReservoirProperties.from_orm(values)
            new_values["properties"] = properties
        
        if "id" not in values.keys():
            assert "reservoir_id" in values.keys(), "expecting either 'id' or 'reservoir_id'"
            new_values["id"] = values["reservoir_id"]
        
        for attribute in cls.schema()["properties"].keys():
            if attribute in values.keys():
                new_values[attribute] = attribute

        return {**new_values, **values}
