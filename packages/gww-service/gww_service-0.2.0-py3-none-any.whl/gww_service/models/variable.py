from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from gww_service.database import Base


class Variable(Base):
    __tablename__ = "variables"

    variable_id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    time_series = relationship(
        "TimeSeries",
        back_populates="variable",
        cascade="save-update, delete, delete-orphan, merge, expunge",
        passive_deletes=True
    )

    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    unit = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f"Variable(variable_id={self.variable_id!r}, name={self.name!r}, unit={self.unit!r})"
