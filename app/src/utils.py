# -------------------------------------------------------------------------- #
# Title: Utility Functions for Streamlit App
# Description: This file contains all utility functions for the Streamlit app.
# Author: Thomas Moesl
# Date: March 2025
# -------------------------------------------------------------------------- #

# ------------------ Import Libraries ------------------ #
# Import the required libraries
import pandas as pd
import requests
from pydantic import ValidationError

from src.config import PredictRequest


# ------------------ Utility Functions ----------------- #
# Function to make a prediction request to the API
def make_prediction_request(data, api_url="http://localhost:8000/predict/"):
    """
    Make a prediction request to the API.

    Args:
        data: Data to send to the API
        api_url: The URL of the prediction API endpoint

    Returns:
        tuple: (success, prediction, probability, error_message)
    """
    try:
        response = requests.post(
            api_url,
            json=data,
            timeout=10,
        )
        if response.status_code == 200:
            prediction = response.json().get("prediction")
            probability = response.json().get("probability")
            return True, prediction, probability, None
        else:
            return False, None, None, f"Error in prediction: {response.status_code}"

    except requests.exceptions.RequestException as e:
        return False, None, None, f"Backend API request error: {e}"


# Function to process and validate input data
def process_validate_input_data(data):
    """
    Process and validate input data through Pydantic model.

    Args:
        data: Raw input data (dict or list of dicts)

    Returns:
        tuple: (processed_data, error_message)
    """
    try:
        # Ensure the data is in the correct format (list of dictionaries)
        if isinstance(data, dict):
            data = [data]

        # Validate the JSON structure using Pydantic
        validated_data = [PredictRequest(**entry) for entry in data]

        # Serialize the data for API request
        processed_data = [entry.model_dump() for entry in validated_data]

        return processed_data, None

    except ValidationError as e:
        return None, f"Validation error: {e}"
    except Exception as e:
        return None, f"Error processing data: {str(e)}"


# Function to combine input data, predictions, and probabilities into a DataFrame
def combine_data(input_data, predictions, probabilities):
    """
    Combines input data with model predictions and their probabilities into a single DataFrame.

    Args:
        input_data: List of dictionaries containing input features
        predictions: List of prediction values (0 or 1)
        probabilities: List of probability arrays

    Returns:
        tuple: (dataframe, error_message)
    """
    try:
        # Check for None inputs
        if input_data is None or predictions is None or probabilities is None:
            return None, "Missing input data, predictions, or probabilities"

        # Check if lengths match
        if len(input_data) != len(predictions) or len(input_data) != len(probabilities):
            return (
                None,
                "Length mismatch between input data, predictions, and probabilities",
            )

        # Handle empty input case
        if len(input_data) == 0 and len(predictions) == 0 and len(probabilities) == 0:
            return pd.DataFrame(), None  # Return empty DataFrame with no error

        # Create DataFrame from input data
        df = pd.DataFrame(input_data)

        # Add predictions and probabilities
        df["prediction"] = predictions
        df["probability"] = [
            prob[pred] for pred, prob in zip(predictions, probabilities)
        ]

        return df, None  # Return DataFrame with no error

    except Exception as e:
        return None, f"Error combining data: {e}"


# Function to display download buttons for CSV and JSON exports
def export_data(data):
    """
    Exports the DataFrame to CSV and JSON formats.

    Args:
        data: DataFrame to export

    Returns:
        tuple: (csv_data, json_data, error_message)
    """
    try:
        if data is None:
            return None, None, "No data provided"

        export_file_csv = data.to_csv(index=False)
        export_file_json = data.to_json(orient="records")

        return export_file_csv, export_file_json, None

    except Exception as e:
        return None, None, f"Error exporting data: {e}"


# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
