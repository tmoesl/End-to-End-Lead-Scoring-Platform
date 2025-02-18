# ------------------ Streamlit App for ML Model Prediction ----------------- #
# Title: Streamlit App for ML Model Prediction
# Description: App to interact with a trained Random Forest model via FastAPI.
# Author: Thomas Moesl
# Date: February 2025
# -------------------------------------------------------------------------- #


# ------------------ Import Libraries ------------------ #
# Import the required libraries
import os
import json
import streamlit as st
import requests
import pandas as pd
from pydantic import ValidationError

# ------------------ Import Custom Modules ------------- #
# Import class, style configuration and utility functions
from src.config import PredictRequest
from src.style import STYLE_CONFIG, init_page_style, display_divider, display_footer
from src.utils import combine_data, export_data, show_export_buttons


# ------------------ FastAPI Endpoint ------------------ #
# Define the FastAPI endpoint
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://backend:8000/predict/")


# ------------------ Page Configuration ---------------- #
# Extract style configuration
convert_color = STYLE_CONFIG["CONVERT_COLOR"]
not_convert_color = STYLE_CONFIG["NOT_CONVERT_COLOR"]
line_color = STYLE_CONFIG["LINE_COLOR"]

# Initialize page styling
init_page_style()


# ------------------ Streamlit App --------------------- #
# Title
st.title("ML Model | Lead Conversion Prediction")

# Image
try:
    st.image("/app/utils/lcp_banner.png")  # Load image from mounted volume
except Exception as e:
    st.error(f"Error loading banner image: {e}")

# Description
st.markdown(
    """
    This app utilizes an optimized Random Forest model to predict lead conversion for an EdTech startup,
    helping prioritize high-potential leads. By identifying key conversion drivers—such as website
    engagement, initial interaction channels, and profile completion—the model enables data-driven
    resource allocation to boost conversion rates and optimize marketing strategies.

    ## App Features
    - **Input Lead Data**: Enter lead details manually or upload a JSON file.
    - **Make API Requests**: The app sends the input data to a trained Random Forest model.
    - **Generate Predictions**: The model analyses lead data to assess conversion potential.
    - **Export Results**: Save predictions as a CSV file for further analysis and decision-making.

    ## Business Impact
    - **Enhanced Lead Prioritization**: Focus on high-conversion leads to maximize ROI.
    - **Optimized Marketing Strategies**: Tailor campaigns based on key conversion drivers.
    - **Data-Driven Decision-Making**: Leverage insights to refine sales and marketing efforts.

    ## Instructions
    1. Select the method of data input: manual input or JSON file upload.
    2. Enter lead details or upload a JSON file containing multiple leads.
    3. Click the 'Predict' button to generate conversion predictions.
    4. View the prediction results and export the data for further analysis.
    """,
    unsafe_allow_html=True,
)

# Horizontal line
display_divider()

# Select Data Input Method
st.markdown("## Select Data Input Method")

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
display_divider()

if input_method == "Upload JSON":

    # Ensure data_to_send is initialized
    data_to_send = None

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
        if data_to_send is None:
            st.warning("Please upload a valid JSON file.")
            st.stop()

        try:
            response = requests.post(
                FASTAPI_URL,
                json=data_to_send,
                timeout=10,
            )
            if response.status_code == 200:
                prediction = response.json().get("prediction")
                probability = response.json().get("probability")
                st.success("Prediction successful!")

                # Display distribution of predictions
                prediction_series = pd.Series(prediction)
                value_counts = prediction_series.value_counts().to_dict()

                # Calculate percentages
                total_count = len(prediction)
                total = sum(value_counts.values())
                percentage_0 = value_counts.get(0, 0) / total * 100
                percentage_1 = value_counts.get(1, 0) / total * 100

                st.markdown(
                    f"""
                    <div class="custom-card">
                        <div class="custom-title">Distribution of Predictions</div>
                        <div class="custom-subtitle">Leads are likely to:</div>
                        <div style="display: flex; justify-content: center; gap: 100px;">
                            <div style="text-align: center;">
                                <span class="not-convert">NOT CONVERT</span>
                                <div style="font-size: 24px; margin-top: 10px;">
                                    {value_counts[0]} ({percentage_0:.1f}%)
                                </div>
                            </div>
                            <div style="text-align: center;">
                                <span class="convert">CONVERT</span>
                                <div style="font-size: 24px; margin-top: 10px;">
                                    {value_counts[1]} ({percentage_1:.1f}%)
                                </div>
                            </div>
                        </div>
                        </br>
                        <div style="text-align: center; 
                                font-size: 20px;
                                font-style: italic;
                                color: var(--text-color);
                                margin-bottom: 10px;">
                            Total number of predictions: {total_count}
                        </div>
                    </div>
                    <br>
                    """,
                    unsafe_allow_html=True,
                )

                # Create a DataFrame with input data, predictions and probabilities
                results_df = combine_data(data_to_send, prediction, probability)

                with st.expander("See prediction output and associated probability"):
                    # Display the table
                    st.write(results_df.loc[:, ["prediction", "probability"]])

                # Export data to CSV or JSON
                export_file_csv, export_file_json = export_data(results_df)
                show_export_buttons(export_file_csv, export_file_json)

            else:
                st.error(f"Error in prediction: {response.status_code}")

        except requests.exceptions.RequestException as e:
            st.error(f"Backend API request error: {e}")
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
        default=["Digital Media Ads"],
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
        try:
            response = requests.post(FASTAPI_URL, json=data_to_send, timeout=10)

            if response.status_code == 200:
                prediction = response.json().get("prediction")
                probability = response.json().get("probability")
                st.success("Prediction successful!")

                # Display prediction result with formatted HTML
                st.markdown(
                    f"""
                    <div class="custom-card">
                        <div class="custom-title">Prediction Result</div>
                        <div class="custom-subtitle">Lead is likely to:</div>
                        <span class="prediction-text" style="color: {convert_color if prediction[0] == 1 else not_convert_color};">
                            {'CONVERT' if prediction[0] == 1 else 'NOT CONVERT'}
                        </span>
                        <div class="probability-text">
                            Estimated probability of {'converting' if prediction[0] == 1 else 'not converting'}: 
                            {probability[0][1]*100 if prediction[0] == 1 else probability[0][0]*100:.1f}%
                        </div>
                    </div>
                    <br>
                    """,
                    unsafe_allow_html=True,
                )

                # Create a DataFrame with input data, predictions and probabilities
                results_df = combine_data(data_to_send, prediction, probability)

                with st.expander("See prediction output and associated probability"):
                    # Display the table
                    st.write(results_df.loc[:, ["prediction", "probability"]])

                # Export data to CSV or JSON
                export_file_csv, export_file_json = export_data(results_df)
                show_export_buttons(export_file_csv, export_file_json)

            else:
                st.error(f"Error in prediction: {response.status_code}")

        except requests.exceptions.RequestException as e:
            st.error(f"Backend API request error: {e}")


# ------------------ Footer Section -------------------- #
# Horizontal line
display_divider()

# Footer with copyright and timestamp
display_footer()

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
