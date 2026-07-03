import joblib
import pandas as pd
from prediction.predict_models import PredictResponse, PredictRequest

decision_tree = joblib.load("prediction/models/decision_tree_model.pkl")
linear_regression = joblib.load("prediction/models/linear_regression_model.pkl")
random_forest = joblib.load("prediction/models/random_forest_model.pkl")

async def execute(data: PredictRequest) -> PredictResponse:
  df = pd.DataFrame([{
    "TipoTrabajo": data.job_type,
    "Cantidad": data.quantity,
    "Tamaño": data.size,
    "Material": data.material,
    "Color": data.isColored
  }])

  selected_model = None
  match data.model:
    case "linear_regression": 
      selected_model = linear_regression
    case "random_forest":
      selected_model = random_forest
    case "decision_tree":
      selected_model = decision_tree

  time = float(selected_model.predict(df)[0])

  return PredictResponse(
    model = data.model,
    estimated_time = time
  )