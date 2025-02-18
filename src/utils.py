# -------------------------------------------------------------------------- #
# Title: Utility Functions for Streamlit App
# Description: This file contains all utility functions for the Streamlit app.
# Author: Thomas Moesl
# Date: February 2025
# -------------------------------------------------------------------------- #

# ------------------ Import Libraries ------------------ #
# Import the required libraries
import pandas as pd
import streamlit as st


# ------------------ Utility Functions ----------------- #
# Function to combine input data, predictions, and probabilities into a DataFrame
def combine_data(input_data, predictions, probabilities):
    """Combines input data with model predictions and their probabilities into a single DataFrame."""
    try:
        df = pd.DataFrame(input_data)
        df["prediction"] = predictions
        df["probability"] = [
            prob[pred] for pred, prob in zip(predictions, probabilities)
        ]  # Prediction [0, 1]
        return df
    except Exception as e:
        st.error(f"Error combining data: {e}")
        return None


# Function to display download buttons for CSV and JSON exports
def export_data(data):
    """Exports the DataFrame to CSV and JSON formats."""
    try:
        export_file_csv = data.to_csv(index=False)
        export_file_json = data.to_json(orient="records")
        return export_file_csv, export_file_json
    except Exception as e:
        st.error(f"Error exporting data: {e}")
        return None


# Function to create download buttons for CSV and JSON
def show_export_buttons(export_file_csv, export_file_json):
    """Displays download buttons for CSV and JSON files."""
    st.write("")  # Add vertical space

    # Create a centered container
    with st.container():
        # Use columns to center the buttons as a unit
        spacer_col, buttons_col, spacer_col2 = st.columns([1.6, 2.8, 1.6])

        with buttons_col:  # This column holds both buttons together
            btn1_col, btn2_col = st.columns([1, 1])  # Equal spacing between buttons

            with btn1_col:
                st.download_button(
                    label="Export to CSV",
                    data=export_file_csv,
                    file_name="predictions.csv",
                    mime="text/csv",
                )

            with btn2_col:
                st.download_button(
                    label="Export to JSON",
                    data=export_file_json,
                    file_name="predictions.json",
                    mime="application/json",
                )


# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
