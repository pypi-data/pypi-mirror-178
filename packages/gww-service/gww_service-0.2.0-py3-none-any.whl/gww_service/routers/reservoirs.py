from datetime import datetime
from logging import getLogger
from logging.config import dictConfig
from typing import List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query, Path
from geojson_pydantic.geometries import Geometry
from sqlalchemy.engine.row import Row
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from gww_service import crud, schemas, models
from gww_service.database import SessionLocal
from gww_service.config import LogConfig
from gww_service.schemas.time_series import (
    AggPeriodEnum,
    AggregatedTimeSeries,
    TimeSeriesElement,
    TimeSeriesReservoirElement,
    TimeSeriesUnits,
)

dictConfig(LogConfig().dict())
logger = getLogger("gww-service")

router: APIRouter = APIRouter(
    prefix="/reservoir",
    tags=["reservoir"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Reservoir CRUD

@router.get("/", response_model=List[schemas.Reservoir])
def list_reservoirs(
    skip: int = Query(
        0,
        description="number of items to skip",
        ge=0
    ),
    limit: int = Query(
        5,
        description="max number of responses",
        gt=0
    ),
    db: Session = Depends(get_db)
):
    """
    List all reservoirs in the database. Because of the high volume, it is recommended to limit
    your query. And make multiple queries, skipping the previous requests.
    """
    db_reservoirs: List[models.Reservoir] = crud.list_reservoirs(db=db, skip=skip, limit=limit)
    return db_reservoirs

@router.get("/{reservoir_id}", response_model=schemas.Reservoir)
def get_reservoir_by_id(
    reservoir_id: int = Path(
        ...,
        description="unique reservoir id",
        gt=0,
    ),
    db: Session = Depends(get_db)
):
    """
    Get one reservoir by their unqique id.
    """
    db_reservoir: models.Reservoir = crud.get_reservoir(db=db, reservoir_id=reservoir_id)
    if db_reservoir is None:
        raise HTTPException(status_code=400, detail="Reservoir not found")
    return db_reservoir

@router.post("/geometry", response_model=List[schemas.Reservoir])
def get_reservoirs_intersects_geom(
    geometry: Geometry = Body(
        ...,
        description="geojson Geometry object",
        example={
            "type": "Polygon",
            "coordinates": [
                [
                    [
                        15.97412109375,
                        49.0880329436187
                    ],
                    [
                        16.194190979003906,
                        49.0880329436187
                    ],
                    [
                        16.194190979003906,
                        49.20503726723141
                    ],
                    [
                        15.97412109375,
                        49.20503726723141
                    ],
                    [
                        15.97412109375,
                        49.0880329436187
                    ]
                ]
            ]
        }
    ),
    db: Session = Depends(get_db)
):
    """
    Get all reservoirs that intersect with the posted geometry. Good for examining which
    reservoirs lie within the requesters area of interest.
    The posted geometry should be a valid geojson.

    See:
        https://postgis.net/docs/ST_Intersects.html
    """
    return crud.get_reservoirs_intersects_geom(db=db, geometry=geometry)

@router.post("/geometry/ts/{variable_name}", response_model=schemas.AggregatedTimeSeries)
def get_timeseries_for_geometry(
    variable_name: str = Path(
        ...,
        description="name of the variable you want to query",
        example="surface_water_area"
    ),
    geometry: Geometry = Body(
        ...,
        description="geojson Geometry object",
        example={
            "type": "Polygon",
            "coordinates": [
                [
                    [
                        15.97412109375,
                        49.0880329436187
                    ],
                    [
                        16.194190979003906,
                        49.0880329436187
                    ],
                    [
                        16.194190979003906,
                        49.20503726723141
                    ],
                    [
                        15.97412109375,
                        49.20503726723141
                    ],
                    [
                        15.97412109375,
                        49.0880329436187
                    ]
                ]
            ]
        }
    ),
    agg_period: AggPeriodEnum = Query(
        ...,
        description="Aggregation timescale",
        example=AggPeriodEnum.MONTHLY.value,
    ),
    start: Optional[datetime] = Query(
        default=None,
        description="Start time of timeseries.",
        example="2020-01-01T00:00:00"
    ),
    stop: Optional[datetime] = Query(
        default=None,
        description="Stop time of timeseries.",
        example="2021-01-01T00:00:00"
    ),
    db: Session = Depends(get_db)
):
    # count number of reservoirs in geom
    reservoirs: List[models.Reservoir] = crud.get_reservoirs_intersects_geom(db, geometry)
    count = len(reservoirs)
    if count == 0:
        raise HTTPException(status_code=400, detail="no reservoirs in geom")
    else:
        try:
            variable: models.Variable = crud.get_variable_from_name(db, variable_name)
        except NoResultFound as e:
            raise HTTPException(400, f"variable with name {variable_name} not found")
        agg_ts: List[Row] = crud.get_reservoirs_timeseries_sum(
            db=db,
            variable_name=variable_name,
            aggregation_period=agg_period,
            reservoir_ids=list(map(lambda res: res.reservoir_id, reservoirs)),
            start=start,
            stop=stop,
        )
        agg_ts_schema: List[TimeSeriesElement] = [
            TimeSeriesElement.from_orm(row) for row in agg_ts
        ]

        split_ts = None
        if count < 10:
            raw_ts: List[Row] = crud.get_reservoirs_timeseries(
                db=db,
                reservoir_ids=list(map(lambda res: res.reservoir_id, reservoirs)),
                variable_id=variable.variable_id,
                start=start,
                stop=stop,
            )
            raw_res_ts_schema: List[TimeSeriesReservoirElement] = [
                TimeSeriesReservoirElement.from_orm(row) for row in raw_ts
            ]

            # split per reservoir
            split_ts = {}

            for r_el in raw_res_ts_schema:
                split_ts.setdefault(r_el.reservoir_id, []).append(TimeSeriesElement(t=r_el.t, value=r_el.value))

        return AggregatedTimeSeries(
            agg_period=agg_period,
            variable_name=variable_name,
            variable_unit=variable.unit,
            data=agg_ts_schema,
            source_data=split_ts,
        )

# # TODO: omitting the post/put/delete records for now as we do not have authentication.
# @router.post("/", response_model=schemas.Reservoir)
# def create(reservoir: schemas.ReservoirCreate, db: Session = Depends(get_db)):
#     return crud.create_reservoir(db=db, reservoir=reservoir)  

# @router.put("/{reservoir_id}", response_model=schemas.Reservoir)
# def update(
#     reservoir_id: int,
#     reservoir: schemas.ReservoirCreate,
#     response: Response,
#     db: Session = Depends(get_db)
# ):
#     db_reservoir = crud.get_reservoir(db=db, reservoir_id=reservoir_id)
#     if db_reservoir is None:
#         response.status_code=status.HTTP_201_CREATED
#         return crud.create_reservoir(db=db, reservoir=reservoir)
#     return crud.update_reservoir(db=db, reservoir=reservoir, id=reservoir_id)

# @router.delete("/{reservoir_id}", status_code=status.HTTP_202_ACCEPTED)
# def delete(reservoir_id: int, db: Session = Depends(get_db)):
#     crud.delete_reservoir(db=db, reservoir_id=reservoir_id)

# Relations

@router.get("/{reservoir_id}/ts", response_model=List[schemas.TimeSeriesUnits])
def get_all_reservoir_timeseries(
    reservoir_id: int = Path(
        ...,
        description="unique reservoir id",
        gt=0
    ),
    start: Optional[datetime] = Query(
        default=None,
        description="Start time of timeseries.",
        example="2020-01-01T00:00:00"
    ),
    stop: Optional[datetime] = Query(
        default=None,
        description="Stop time of timeseries.",
        example="2021-01-01T00:00:00"
    ),
    db: Session = Depends(get_db)
) -> List[Row]:
    rts: List[Row] = crud.get_all_reservoir_timeseries(db, reservoir_id, start, stop)
    return [TimeSeriesUnits.from_orm(rs) for rs in rts]

@router.get("/{reservoir_id}/ts/{variable_name}", response_model=List[schemas.TimeSeriesUnits])
def get_reservoir_timeseries(
    reservoir_id: int = Path(
        ...,
        description="unique reservoir id",
        gt=0
    ),
    variable_name: Optional[str] = Path(
        None,
        description="optional name of the variable that will be queried for",
        example="surface_water_area"
    ),
    start: Optional[datetime] = Query(
        default=None,
        description="Start time of timeseries.",
        example="2020-01-01T00:00:00"
    ),
    stop: Optional[datetime] = Query(
        default=None,
        description="Stop time of timeseries.",
        example="2021-01-01T00:00:00"
    ),
    db: Session = Depends(get_db)
) -> List[schemas.TimeSeriesUnits]:
    """
    Get the time series for a single reservoir. You can optionally add the variable name to just
    query a single variable, otherwise all variables are given.
    """
    ts: List[Row] = crud.get_reservoir_timeseries(db, reservoir_id, variable_name, start, stop)
    return [TimeSeriesUnits.from_orm(s) for s in ts]

