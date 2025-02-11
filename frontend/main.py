# ------------------ Streamlit App for ML Model Prediction ----------------- #
# Author: Thomas Moesl
# Date: February 2025
# Description: App to interact with a trained Random Forest model via FastAPI.
# -------------------------------------------------------------------------- #


# ------------------ Import Libraries ------------------ #
# Import the required libraries
import os
import streamlit as st
import requests
import json
import pandas as pd
import datetime
from pydantic import ValidationError
from src.config import PredictRequest  # Import the PredictRequest class


# ------------------ Utility Functions ----------------- #
# Function to export input data and predictions to CSV
def export_to_csv(input_data, predictions):
    try:
        df = pd.DataFrame(input_data)
        df["prediction"] = predictions
        return df.to_csv(index=True, index_label="index")
    except Exception as e:
        st.error(f"Error exporting to CSV: {e}")
        return None


# ------------------ FastAPI Endpoint ------------------ #
# Define the FastAPI endpoint
# Define the FastAPI endpoint (default: fallback for local development without Docker)
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000/predict/")

# ------------------ Streamlit App --------------------- #
# Set page style
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    
    /* Adjust text sizes */
    h1 { font-size: 34px !important; }  /* Title size (1.4x h2) */
    h2 { font-size: 26px !important; }  /* Subtitle size (1.3x h3) */
    h3 { font-size: 22px !important; }  /* Section heading */
    p, li, div { font-size: 18px !important; }  /* Body text */

    </style>
    """,
    unsafe_allow_html=True,
)

# Title
st.title("ML Model | Lead Conversion Prediction")

# Banner image
try:
    st.image("/app/utils/lcp_banner.png")  # Load image from mounted volume
except Exception as e:
    st.error(f"Error loading banner image: {e}")

# Description of the app
st.markdown(
    """
This app utilizes an optimized Random Forest model to predict lead conversion for an EdTech startup, 
helping prioritize high-potential leads. By identifying key conversion drivers—such as website engagement,
initial interaction channels, and profile completion—the model enables data-driven resource allocation to 
boost conversion rates and optimize marketing strategies.

#### App Features
- **Input Lead Data**: Enter lead details manually or upload a JSON file.
- **Make API Requests**: The app sends the input data to a trained Random Forest model.
- **Generate Predictions**: The model analyzes lead data to assess conversion potential.
- **Export Results**: Save predictions as a CSV file for further analysis and decision-making.
"""
)

# Legend for prediction values
st.markdown(
    """
    <div style="color: white; background-color: #2E2F38; padding: 10px; border-radius: 5px; border: 1px solid white;">
        <strong>Model Output</strong>
        <ul>
            <li><strong>0</strong>: Low Conversion Potential – Lower priority for follow-up.</li>
            <li><strong>1</strong>: High Conversion Potential – Prioritize for engagement.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

# Horizontal line
st.markdown("<hr style='border: 1px solid white;'>", unsafe_allow_html=True)

# Select Data Input Method
st.markdown("#### Select Data Input Method")

input_method = st.radio(
    "Enter data manually or upload a JSON file:",
    ("Manual Input", "Upload JSON"),
    index=0,
    help="**Manual Input**: Enter the data manually through the provided input fields. \
    \n**Upload JSON**: Upload a JSON file containing the data.",
)

if input_method == "Upload JSON":
    # Display a preview of the expected JSON format
    with st.expander("Preview expected JSON format"):
        sample_json = [
            {
                "age": 57,
                "website_visits": 1,
                "time_spent_on_website": 582,
                "page_views_per_visit": 2.197,
                "current_occupation_student": False,
                "current_occupation_unemployed": False,
                "first_interaction_website": False,
                "profile_completed_low": False,
                "profile_completed_medium": False,
                "last_activity_phone": False,
                "last_activity_website": False,
                "print_media_type1_yes": False,
                "print_media_type2_yes": False,
                "digital_media_yes": False,
                "educational_channels_yes": True,
                "referral_yes": False,
            },
            {
                "age": 36,
                "website_visits": 2,
                "time_spent_on_website": 1937,
                "page_views_per_visit": 5.111,
                "current_occupation_student": False,
                "current_occupation_unemployed": True,
                "first_interaction_website": True,
                "profile_completed_low": False,
                "profile_completed_medium": True,
                "last_activity_phone": False,
                "last_activity_website": False,
                "print_media_type1_yes": False,
                "print_media_type2_yes": False,
                "digital_media_yes": True,
                "educational_channels_yes": False,
                "referral_yes": False,
            },
        ]
        st.code(json.dumps(sample_json, indent=4), language="json")

# Horizontal line
st.markdown("<hr style='border: 1px solid white;'>", unsafe_allow_html=True)

if input_method == "Upload JSON":
    # File uploader for JSON input
    uploaded_file = st.file_uploader("Choose a JSON file", type="json")

    if uploaded_file is not None:
        try:
            # Read and parse the JSON file
            data = json.load(uploaded_file)

            # Ensure the data is in the correct format (list of dictionaries)
            if isinstance(data, dict):
                data = [data]

            # Validate the JSON structure using Pydantic
            validated_data = [PredictRequest(**entry) for entry in data]

            # Serialize the data for API request
            data_to_send = [entry.model_dump() for entry in validated_data]

            # Display the data for API request
            with st.expander("Preview data to be sent to API"):
                st.write(data_to_send)

        except json.JSONDecodeError:
            st.error("Invalid JSON file. Please upload a valid JSON file.")
        except ValidationError as e:
            st.error(f"Validation error: {e}")

    else:
        st.info("Please upload a JSON file.")

    # Button to make prediction
    if st.button("Predict"):
        response = requests.post(
            FASTAPI_URL,
            json=data_to_send,
            timeout=10,
        )
        if response.status_code == 200:
            prediction = response.json().get("prediction")
            st.success("Prediction successful!")

            # Display distribution of predictions
            prediction_series = pd.Series(prediction)
            value_counts = prediction_series.value_counts().sort_index()

            # Display total number of predictions
            total_count = len(prediction)
            st.write(f"Total Number: {total_count}")

            chart = st.bar_chart(value_counts)

            with st.expander("See detailed prediction output"):
                st.write(f"{prediction}")

            # Export input data and predictions to CSV
            csv = export_to_csv(data_to_send, prediction)
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name="predictions.csv",
                mime="text/csv",
            )

        else:
            st.error(f"Error in prediction: {response.status_code}")

else:
    # --- Numerical Inputs --- #
    age = st.number_input(
        "Age",
        min_value=0,
        max_value=100,
        value=50,
        step=1,
        help="Enter the age of the lead (0-100 years).",
    )
    website_visits = st.number_input(
        "Number of Website Visits",
        min_value=0,
        value=5,
        step=1,
        help="Enter the total number of visits to the website.",
    )
    time_spent_on_website = st.number_input(
        "Total Time Spent on Website (seconds)",
        min_value=0,
        value=180,
        step=1,
        help="Enter the total time spent on the website in seconds.",
    )
    page_views_per_visit = st.number_input(
        "Page Views per Visit",
        min_value=0.0,
        value=2.5,
        step=0.1,
        help="Enter the average number of pages viewed per visit.",
    )

    # --- Categorical Inputs (Dropdowns) --- #
    current_occupation = st.selectbox(
        "Current Occupation",
        ["Professional", "Unemployed", "Student"],
        index=0,
        help="Select the current occupation of the lead.",
    )
    first_interaction = st.selectbox(
        "First Interaction Channel",
        ["Website", "Mobile App"],
        index=0,
        help="Select the first interaction channel with the lead.",
    )
    profile_completed = st.selectbox(
        "Profile Completion Level",
        ["Low (0-50%)", "Medium (50-75%)", "High (75-100%)"],
        index=0,
        help="Select the level of profile completion for the lead.",
    )
    last_activity = st.selectbox(
        "Most Recent Interaction",
        ["Email", "Phone", "Website"],
        index=0,
        help="Select the most recent interaction with the lead.",
    )
    referral_yes = st.selectbox(
        "Referred by Others",
        ["Yes", "No"],
        index=0,
        help="Select if the lead was referred by others.",
    )

    # --- Multi-select Input --- #
    media_types = st.multiselect(
        "Seen via Media or Education Channels",
        [
            "Print Media Type 1",
            "Print Media Type 2",
            "Digital Media Ads",
            "Educational Channels",
        ],
        help="Select the media or education channels through which the lead was acquired.",
    )

    # Prepare data dictionary for API request
    data = {
        "age": age,
        "website_visits": website_visits,
        "time_spent_on_website": time_spent_on_website,
        "page_views_per_visit": page_views_per_visit,
        "current_occupation_student": current_occupation == "Student",
        "current_occupation_unemployed": current_occupation == "Unemployed",
        "first_interaction_website": first_interaction == "Website",
        "profile_completed_low": profile_completed == "Low (0-50%)",
        "profile_completed_medium": profile_completed == "Medium (50-75%)",
        "last_activity_phone": last_activity == "Phone",
        "last_activity_website": last_activity == "Website",
        "print_media_type1_yes": "Print Media Type 1" in media_types,
        "print_media_type2_yes": "Print Media Type 2" in media_types,
        "digital_media_yes": "Digital Media Ads" in media_types,
        "educational_channels_yes": "Educational Channels" in media_types,
        "referral_yes": referral_yes == "Yes",
    }

    try:
        # Validate the data using Pydantic
        validated_data = PredictRequest(**data)

        # Serialize the data for API request
        data_to_send = [validated_data.model_dump()]

        # Display the data for API request
        with st.expander("Preview data sent to API"):
            st.write(data_to_send)

    except ValidationError as e:
        st.error(f"Validation error: {e}")

    # Button to make prediction
    if st.button("Predict"):
        response = requests.post(FASTAPI_URL, json=data_to_send, timeout=10)

        if response.status_code == 200:
            prediction = response.json().get("prediction")
            st.success(f"Prediction: {prediction}")

            # Export input data and predictions to CSV
            csv = export_to_csv(data_to_send, prediction)
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name="predictions.csv",
                mime="text/csv",
            )
        else:
            st.error(f"Error in prediction: {response.status_code}")


# ------------------ Footer Section -------------------- #
# Horizontal line
st.markdown("<hr style='border: 1px solid white;'>", unsafe_allow_html=True)

# Footer with copyright and timestamp
current_year = datetime.datetime.now().year
st.markdown(
    f"""
    <div style="text-align: center; font-size: small; color: gray;">
        &copy; {current_year} Thomas Moesl. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
