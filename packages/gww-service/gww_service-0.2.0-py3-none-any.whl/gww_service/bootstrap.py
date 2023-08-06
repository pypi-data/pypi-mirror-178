from gww_service.database import Base, engine
from gww_service.earthengine import ee_init

from gww_service.config import settings

def bootstrap():
    # TODO: if using repository pattern, inject dependencies
    Base.metadata.create_all(bind=engine)
    if settings.use_ee:
        ee_init()
