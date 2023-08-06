from datetime import datetime
from typing import List, Optional

from geojson_pydantic.geometries import Geometry
from sqlalchemy import func, select
from sqlalchemy.engine.row import Row
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select

from gww_service import models, schemas
from gww_service.schemas.time_series import AggPeriodEnum
from gww_service.crud.variable import get_variable_id_from_name

def filter_start_stop(statement: Select, start: Optional[datetime]=None, stop: Optional[datetime]=None):
    if start:
        statement = statement.where(models.TimeSeries.t >= start)
    if stop:
        statement = statement.where(models.TimeSeries.t < stop)
    return statement

def get_reservoir(db: Session, reservoir_id: int) -> Optional[models.Reservoir]:
    return db \
        .query(models.Reservoir) \
        .where(models.Reservoir.reservoir_id == reservoir_id) \
        .first()

def list_reservoirs(db: Session, skip: int = 0, limit: int = 100) -> List[models.Reservoir]:
    return db \
        .query(models.Reservoir) \
        .offset(skip).limit(limit).all()

def get_reservoirs_intersects_geom(db: Session, geometry: Geometry) -> List[models.Reservoir]:
    return db \
        .query(models.Reservoir) \
        .filter(models.Reservoir.geometry.ST_Intersects(geometry.wkt)) \
        .all()

def get_reservoirs_intersects_geom_count(db: Session, geometry: Geometry) -> int:
    return db \
        .query(models.Reservoir) \
        .filter(models.Reservoir.geometry.ST_Intersects(geometry.wkt)) \
        .count()

def create_reservoir(db: Session, reservoir: schemas.ReservoirCreate) -> models.Reservoir:
    db_reservoir: models.Reservoir = models.Reservoir.from_schema(reservoir)
    db.add(db_reservoir)
    db.commit()
    db.refresh(db_reservoir)
    return db_reservoir

def update_reservoir(db: Session, reservoir: schemas.ReservoirCreate, id: int) -> models.Reservoir:
    reservoir_sqalchemy = models.Reservoir.from_schema(reservoir)
    db_reservoir: models.Reservoir = get_reservoir(db, reservoir_id=id)
    for colname in reservoir_sqalchemy.__table__.columns.keys():
        if colname == "reservoir_id":  # cannot set id
            continue
        setattr(db_reservoir, colname, getattr(reservoir_sqalchemy, colname))
    
    db.commit()
    db.refresh(db_reservoir)
    return db_reservoir

def delete_reservoir(db: Session, reservoir_id: int) -> None:
    db.query(models.Reservoir).filter(models.Reservoir.reservoir_id == reservoir_id).delete()
    db.commit()

def get_reservoir_ts_units(
    reservoir_id: int,
    start: Optional[datetime] = None,
    stop: Optional[datetime] = None,
) -> Select:
    """
    generate statement for getting the timeseries plus their units for a single reservoir.
    """

    # Subquery is used to improve query performance. This strategy is chosen due 
    # to the variable table staying relatively small
    sub_statement: Select = select(
        models.TimeSeries.t,
        models.TimeSeries.value,
        models.TimeSeries.variable_id,
    ) \
        .order_by(models.TimeSeries.t.asc()) \
        .where(models.TimeSeries.reservoir_id == reservoir_id)
    
    sub_statement = filter_start_stop(sub_statement, start, stop)
    sub_statement = sub_statement.subquery()
    
    statement: Select = select(
        sub_statement.c.t,
        sub_statement.c.value,
        models.Variable.variable_id,
        models.Variable.name,
        models.Variable.unit,
    ) \
        .join_from(sub_statement, models.Variable)

    return statement

def get_multi_reservoir_ts_units(
    reservoir_ids: List[int],
    start: Optional[datetime] = None,
    stop: Optional[datetime] = None,
) -> Select:
    """
    generate statement for getting the timeseries plus their units for multiple reservoirs.
    """
    # Subquery is used to improve query performance. This strategy is chosen due 
    # to the variable table staying relatively small
    sub_statement: Select = select(
        models.TimeSeries.reservoir_id,
        models.TimeSeries.t,
        models.TimeSeries.value,
        models.TimeSeries.variable_id,
    ) \
        .order_by(models.TimeSeries.t.asc()) \
        .where(models.TimeSeries.reservoir_id.in_(reservoir_ids))
    
    sub_statement = filter_start_stop(sub_statement, start, stop)
    sub_statement = sub_statement.subquery()
    
    statement: Select = select(
        sub_statement.c.reservoir_id,
        sub_statement.c.t,
        sub_statement.c.value,
        models.Variable.variable_id,
        models.Variable.name,
        models.Variable.unit,
    ) \
        .join_from(sub_statement, models.Variable)

    return statement


def get_reservoir_timeseries(
    db: Session,
    reservoir_id: int,
    variable_name: str,
    start: Optional[datetime] = None,
    stop: Optional[datetime] = None
) -> List[Row]:
    """
    gets reservoir timeseries for one variable, time left-inclusive.
    """
    statement: Select = get_reservoir_ts_units(reservoir_id, start, stop) \
        .where(models.Variable.name == variable_name)
    return db.execute(statement).all()

def get_all_reservoir_timeseries(
    db: Session,
    reservoir_id: int,
    start: Optional[datetime] = None,
    stop: Optional[datetime] = None
) -> List[Row]:
    """
    Gets all reservoir timeseries, time left-inclusive.
    """
    statement: Select = get_reservoir_ts_units(reservoir_id, start, stop)
    return db.execute(statement).all()

def get_reservoirs_timeseries(
    db: Session,
    reservoir_ids: List[int],
    variable_id: int,
    start: Optional[datetime] = None,
    stop: Optional[datetime] = None,
) -> List[Row]:
    """
    Get reservoir timeseries for multiple timeseries.
    """
    statement: Select = get_multi_reservoir_ts_units(reservoir_ids, start, stop) \
        .where(models.Variable.variable_id == variable_id)
    return db.execute(statement).all()

def get_reservoirs_timeseries_sum(
    db: Session,
    variable_name: str,
    aggregation_period: AggPeriodEnum,
    reservoir_ids: List[int],
    start: Optional[datetime] = None,
    stop: Optional[datetime] = None,
) -> List[Row]:
    """
    Gets an aggregate of the reservoir data, time left-inclusive.
    """
    agg_variable_id: models.Variable = get_variable_id_from_name(db, f"{variable_name}_{aggregation_period.value}")

    stmt = select(
        models.TimeSeries.t,
        func.sum(models.TimeSeries.value).label("value")
    ).group_by(models.TimeSeries.t) \
    .order_by(models.TimeSeries.t.asc())

    filtered_stmt = filter_start_stop(stmt, start, stop) \
        .where(models.TimeSeries.variable_id == agg_variable_id) \
        .where(models.TimeSeries.reservoir_id.in_(reservoir_ids))

    return db.execute(filtered_stmt).all()
