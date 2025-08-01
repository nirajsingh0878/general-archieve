from pydantic import BaseModel
from typing import List

# Defines what the input for your prediction should look like
class IrisFeatures(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# Defines what the output of your prediction will look like
class PredictionResponse(BaseModel):
    prediction: int
    class_name: str