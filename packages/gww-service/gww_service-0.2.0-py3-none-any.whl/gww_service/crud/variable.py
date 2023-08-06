from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import Select

from gww_service.models import Variable

def get_variable_id_from_name(session: Session, name: str) -> int:
    """
    Get variable id from the database based on the variable name.

    args:
        session: SQLAlchemy session object.
        name: variable name.
    
    returns:
        variable id
    """
    stmt: Select = select(Variable.variable_id).where(Variable.name == name)
    return session.execute(stmt).scalar_one()

def get_variable_from_name(session: Session, name: str) -> Variable:
    """
    Get variable model from DB based on name.

    args:
        session: SQLAlchemy session object.
        name: variable name.
    
    returns:
        variable model
    """
    stmt: Select = select(Variable).where(Variable.name == name)
    return session.execute(stmt).scalar_one()