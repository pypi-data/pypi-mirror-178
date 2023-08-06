from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel

class AggPeriodEnum(Enum):
    """
    Enumeration describing all periods that we are aggregating data over.
    """
    MONTHLY = "monthly"

class TimeSeriesElement(BaseModel):
    value: float
    t: datetime

    class Config:
        orm_mode = True

class TimeSeriesReservoirElement(TimeSeriesElement):
    """
    Useful when source time series come from multiple reservoirs.
    """
    reservoir_id: int

class TimeSeriesBase(TimeSeriesReservoirElement):
    variable_id: int

class TimeSeriesCreate(TimeSeriesBase):
    pass

class TimeSeries(TimeSeriesBase):
    time_series_id: int
    class Config:
        orm_mode = True

class TimeSeriesUnits(TimeSeriesElement):
    name: str
    unit: str

class ReservoirTimeseries(TimeSeriesUnits):
    reservoir_id: int

class AggregatedTimeSeries(BaseModel):
    """
    Schema returned in route reservoir/geometry/ts
    Contains the aggregated timeseries of a variable and can optionally include its source data.
    """
    agg_period: AggPeriodEnum
    variable_name: str
    variable_unit: str
    data: List[TimeSeriesElement]
    source_data: Optional[Dict[int, List[TimeSeriesElement]]]
