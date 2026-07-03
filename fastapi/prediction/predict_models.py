from pydantic import BaseModel
from typing import Literal

class PredictRequest(BaseModel):
  job_type: Literal["Banner", "Documento", "Flyer", "Plano", "Tarjeta"]
  quantity: int
  size: Literal["A2", "A3", "A4", "Grande"]
  material: Literal["Bond", "Cartulina", "Couche", "Vinil"]
  isColored: bool
  model: Literal["linear_regression", "random_forest", "decision_tree"]

class PredictResponse(BaseModel):
  model: str
  estimated_time: float