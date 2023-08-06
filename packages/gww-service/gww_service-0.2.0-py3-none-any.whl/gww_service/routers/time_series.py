from fastapi import APIRouter

router: APIRouter = APIRouter(
    prefix="/ts",
    tags=["time series"]
)
