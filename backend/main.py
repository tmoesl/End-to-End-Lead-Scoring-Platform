# ---------------------- FastAPI Application ------------------------------- #
# # Author: Thomas Moesl
# Date: February 2025
# Description: FastAPI app for making predictions using a trained model
# -------------------------------------------------------------------------- #


# ---------------- Import Libraries ---------------- #
# Import the required libraries
from fastapi import FastAPI, HTTPException
from typing import List
import pandas as pd
import pickle
import logging
from pydantic import ValidationError
from src.config import PredictRequest  # Import the PredictRequest class

# ---------------- Logging --------------------- #
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------- Load Model ------------------ #
# # Load model from mounted volume
try:
    with open("/app/model/model.pkl", "rb") as f:
        model = pickle.load(f)
except Exception as e:
    logger.error("Error loading model: %s", e)
    raise


# ---------------- FastAPI App ----------------- #
# Initialize FastAPI app
app = FastAPI()


@app.get("/")
def home():
    return {"message": "ML Model API is running"}


@app.post("/predict/")
def predict(request: List[PredictRequest]):
    try:
        # Validate the JSON structure using Pydantic
        validated_data = [PredictRequest(**entry.dict()) for entry in request]

        # Convert validated_data to DataFrame
        input_data = pd.DataFrame([entry.model_dump() for entry in validated_data])

        # Make prediction
        prediction = model.predict(input_data)

        # Logging
        # logger.info("Model expects columns: %s", model.feature_names_in_)
        # logger.info("Streamlit input columns: %s", input_data.columns.tolist())
        # logger.info("Input data: %s", input_data)
        # logger.info("Prediction: %s", prediction)

        return {"prediction": prediction.tolist()}

    except ValidationError as ve:
        logger.error("Validation error: %s", ve)
        raise HTTPException(status_code=400, detail=str(ve)) from ve

    except Exception as e:
        logger.error("Error during prediction: %s", e)
        raise HTTPException(status_code=500, detail="Prediction error") from e


# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #

# ---------------- Additional Code Snippets ---- #

# with open("scaler.pkl", "rb") as scaler_file:
#     scaler = pickle.load(scaler_file)

# Scale numerical features
# numerical_features = input_data.select_dtypes(include=[np.number]).columns

# input_data[numerical_features] = scaler.transform(input_data[numerical_features])
