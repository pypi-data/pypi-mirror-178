from sqlalchemy import Column, DateTime, DDL, event, Float, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from gww_service.database import Base

class TimeSeries(Base):
    __tablename__ = "time_series"

    time_series_id = Column(Integer, primary_key=True, autoincrement=True)

    t = Column(DateTime, primary_key=True)
    value = Column(Float, nullable=False)

    reservoir_id = Column(
        Integer,
        ForeignKey(
            "reservoirs.reservoir_id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )
    variable_id = Column(
        Integer,
        ForeignKey(
            "variables.variable_id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )
    reservoir = relationship("Reservoir", back_populates="time_series")
    variable = relationship("Variable", back_populates="time_series")

    __table_args__ = (
        UniqueConstraint('reservoir_id', 'variable_id', 't', name='_ts_unique_constraint'),
    )

    def __repr__(self):
        return (f"TimeSeries(time_series_id={self.time_series_id!r}, t={self.t!r},"
            f" value={self.value!r})")
    

event.listen(
    TimeSeries.__table__,
    "after_create",
    DDL(f"SELECT create_hypertable('{TimeSeries.__tablename__}', 't')")
)