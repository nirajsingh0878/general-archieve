import pickle
import numpy as np
from fastapi import APIRouter, HTTPException, status
from app.schemas.prediction import IrisFeatures, PredictionResponse
import os # Import os for path handling

# Create a FastAPI router
router = APIRouter()

# --- Model Loading (Simple approach) ---
# Global variables to hold the loaded model and class names
_model = None
_iris_target_names = None

def load_ml_model():
    global _model, _iris_target_names
    # This path is relative to where the script is run from.
    # When running uvicorn from the project root, this path should work.
    model_path = os.path.join(os.path.dirname(__file__), '../models/my_model.pkl')
    try:
        with open(model_path, 'rb') as f:
            _model = pickle.load(f)
        # Load iris dataset just to get target names for demonstration
        from sklearn.datasets import load_iris
        iris = load_iris()
        _iris_target_names = iris.target_names.tolist()
        print(f"ML Model loaded successfully from {model_path}")
    except FileNotFoundError:
        print(f"Error: Model file not found at {model_path}. Make sure to run train_model.py first.")
        _model = None # Ensure model is None if loading fails
    except Exception as e:
        print(f"Error loading ML model: {e}")
        _model = None

# Load model when this module is imported (at app startup)
load_ml_model()

# --- API Endpoint ---
@router.post("/predict", response_model=PredictionResponse)
async def predict_iris_class(features: IrisFeatures):
    """
    Predicts the Iris flower class based on input features.
    """
    if _model is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Machine learning model is not loaded. Server might be misconfigured."
        )

    # Convert Pydantic model to a list for prediction
    feature_list = [
        features.sepal_length,
        features.sepal_width,
        features.petal_length,
        features.petal_width,
    ]

    # Convert list to numpy array and reshape for the model
    input_array = np.array(feature_list).reshape(1, -1)

    try:
        # Make prediction
        prediction_id = _model.predict(input_array)[0]
        # Get the corresponding class name
        class_name = _iris_target_names[prediction_id]

        return PredictionResponse(prediction=int(prediction_id), class_name=class_name)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed due to an internal error: {str(e)}"
        )