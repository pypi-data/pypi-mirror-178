from os import getenv
from typing import Optional

import ee
from eepackages.assets import getImages, getMostlyCleanImages

def ee_init():
    sa_email: Optional[str] = getenv("EE_SA")
    ee_privatekey_path: Optional[str] = getenv("EE_PK")
    if not (sa_email and ee_privatekey_path):
        raise EnvironmentError(
            """
            App requires both 'EE_SA', the service account email for earthengine and 'EE_PK', the
            path to the private key of this service account as environment variables.
            """
        )
    creds = ee.ServiceAccountCredentials(sa_email, ee_privatekey_path)
    ee.Initialize(creds)

def buffer_mask(geometry):
    """
    Compute the mask around the reservoir
    """
    geometry = ee.Geometry(geometry)
    # Mask a region of 1/20 around the reservoir. 
    # we will make this half transparent
    radius = geometry.area().sqrt().divide(10)
    
    # Select a geometry buffered around the reservoir
    outerGeometry = geometry.buffer(radius)
    innerGeometry = geometry
    # The inner geometry 
    # Compute a mask around the inner geometry of size radius
    mask = (ee.FeatureCollection(innerGeometry)
      .distance(radius)
      .paint(innerGeometry, 0)
      .divide(radius)
      .subtract(1)
      .multiply(-1)
      .selfMask()
    )
    return mask

def get_image_for_geometry_t(geometry, t):
    # Lookup latest satellite images for 1 month before t
    # Mosaic them and gradient-mask the outer region

    ee_init()
    geometry = ee.Geometry(geometry)
    t = ee.Date(t)
    
    t1 = ee.Date(t).advance(**{"delta": 1, "unit": "minute"})  # FIXME: remove when database contains minutes
    # go back in time to obtain enough images for quality score
    t0 = t1.advance(**{"delta": -30, "unit": "days"})

    # Get scale based on geometry area  
    scale = geometry.area().sqrt().divide(200).max(10)
    mask = buffer_mask(geometry)
    
    # Get images based on timestamp
    images = getImages(geometry, {
        "missions": ['L4', 'L5', 'L7', 'L8', 'L9', 'S2'],
        "filter": ee.Filter.date(t0, t1),
        "resample": True
    })
    
    # Filter images based on quality score
    images = getMostlyCleanImages(images, geometry, {
        "scale": scale.multiply(5)
    })
    # Get most recent image
    images = images.sort("system:time_start", True)
    
    image = images.mosaic()
    # Apply fading mask
    image = image.mask(mask)
    return image
      