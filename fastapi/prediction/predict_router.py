from fastapi import APIRouter, Request, Response, Query
from prediction.predict_models import PredictRequest, PredictResponse
from prediction import predict_time

router = APIRouter()

@router.get("/")
async def get_prediction(order: PredictRequest = Query()) -> PredictResponse:
 return await predict_time.execute(order)