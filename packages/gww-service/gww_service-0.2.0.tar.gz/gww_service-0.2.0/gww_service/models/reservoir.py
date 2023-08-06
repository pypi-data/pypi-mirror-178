from typing import List, Tuple

from geoalchemy2 import Geometry
from shapely import geometry
from sqlalchemy import Column, Integer, Sequence, String
from sqlalchemy.orm import relationship

from gww_service.database import Base
from gww_service import schemas

RESERVOIR_ID_START = int(1e6)

class Reservoir(Base):
    __tablename__ = "reservoirs"

    # Start of sequence is above existing reservoir ids until this database is source_of_truth
    reservoir_id_seq = Sequence("reservoir_id_seq", metadata=Base.metadata, start=RESERVOIR_ID_START)
    reservoir_id = Column(Integer, reservoir_id_seq, server_default=reservoir_id_seq.next_value(), primary_key=True)
    geometry = Column(Geometry("MULTIPOLYGON", from_text='ST_GeomFromEWKT', spatial_index=True, nullable=False))
    name = Column(String)
    name_en = Column(String)
    grand_id = Column(Integer)
    source_name = Column(String)
    source_id = Column(Integer)

    # At the moment there is no need to eager/lazy load the time series data. Any lazy load strategy will
    # decrease performance everywhere the pydantic reservoir object is inspected. Be cautious.
    time_series = relationship(
        "TimeSeries",
        back_populates="reservoir",
        cascade="save-update, delete, delete-orphan, merge, expunge",
        passive_deletes=True,
        lazy='noload'
    )

    def __repr__(self) -> str:
        return f"Reservoir(reservoir_id={self.reservoir_id!r}, name={self.name})"

    @classmethod
    def from_schema(cls, res: schemas.Reservoir) -> "Reservoir":
        """
        create the reservoir model from the model that we get from 
        """
        res_dict = res.dict()

        def coordinates_to_shapely(coords: List[List[Tuple[float]]]):
            external: List[Tuple[float]] = coords[0]
            internals: List[List[Tuple[float]]] = []
            if len(coords) > 1:
                internals = coords[1:]
            return geometry.Polygon(external, internals)

        polygons: geometry.MultiPolygon = list(map(coordinates_to_shapely, res_dict["geometry"]["coordinates"]))
        res_dict["geometry"] = geometry.MultiPolygon(polygons).wkt
        return Reservoir(
            reservoir_id=res_dict["id"],
            geometry = geometry.MultiPolygon(polygons).wkt,
            name = res_dict["properties"]["name"],
            name_en = res_dict["properties"]["name_en"],
            grand_id = res_dict["properties"]["grand_id"],
            source_name = res_dict["properties"]["source_name"],
            source_id = res_dict["properties"]["source_id"]
        )
