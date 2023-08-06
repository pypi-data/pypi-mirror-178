from typing import Any, Dict, List

from fastapi import FastAPI ,status
import uvicorn
from starlette.responses import RedirectResponse

from gww_service.bootstrap import bootstrap
from gww_service.routers import reservoirs, time_series, images

description: str = """
Api for querying Global Water Watch data and products.
"""

tags_metadata: List[Dict[str, Any]] = [
    {
        "name": "reservoir",
        "description": """
        Operations around the reservoir dataset used by Global Water Watch.
        """
    }
]

app = FastAPI(
    title="Global Water Watch",
    description=description,
    openapi_tags=tags_metadata
)

app.include_router(reservoirs.router)
app.include_router(time_series.router)
app.include_router(images.router)


@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return {"message": "OK"}

@app.get("/", status_code=status.HTTP_308_PERMANENT_REDIRECT)
async def redirect_to_docs():
    response = RedirectResponse(url='/docs')
    return response

@app.on_event("startup")
def startup_event():
    bootstrap()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
