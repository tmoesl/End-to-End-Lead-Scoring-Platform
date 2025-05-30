# ------------------ Streamlit App for ML Model Prediction ----------------- #
# Title: Streamlit App for ML Model Prediction
# Description: App to interact with a trained Random Forest model via FastAPI.
# Author: Thomas Moesl
# Date: March 2025
# -------------------------------------------------------------------------- #


# ------------------ Import Libraries ------------------ #
# Import the required libraries
import json
import os

import pandas as pd
import streamlit as st

# ------------------ Import Custom Modules ------------- #
# Import class, style configuration and utility functions
from src.config import PredictRequest
from src.style import (
    STYLE_CONFIG,
    display_back_to_top,
    display_divider,
    display_export_buttons,
    display_footer,
    display_github_links,
    init_github_links_style,
    init_page_style,
)
from src.template import sample_json
from src.utils import (
    combine_data,
    export_data,
    make_prediction_request,
    process_validate_input_data,
)

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
init_github_links_style()


# ------------------ Header Section -------------------- #
# Title
st.title("ML Model | Lead Conversion Prediction")

# Image
st.markdown(
    '<img src="/app/static/lcp_banner.png" class="rounded-image">',
    unsafe_allow_html=True,
)

# Description Part I
st.markdown(
    """
    This app utilizes an optimized Random Forest model to predict lead conversion for an EdTech startup,
    helping prioritize high-potential leads. By identifying key conversion drivers—such as website
    engagement, initial interaction channels, and profile completion—the model enables data-driven
    resource allocation to boost conversion rates and optimize marketing strategies.
    """,
    unsafe_allow_html=True,
)

# GitHub links
display_github_links()

# Horizontal line
display_divider()

# Description Part II
st.markdown(
    """
    ## App Features
    - **Data Analysis**: Process lead details to evaluate conversion likelihood.
    - **AI-Powered Predictions**: Leverage a trained Random Forest model for real-time insights.
    - **Seamless Export**: Save predictions for easy integration and analysis.

    ## Business Impact
    - **Maximize ROI**: Focus on high-potential leads.
    - **Optimize Marketing**: Tailor campaigns with key conversion drivers.
    - **Drive Decisions**: Utilise data insights to refine sales strategies.

    ## How It Works
    1. Select a data input method and provide lead details.
    2. Click **'Predict'** to generate lead conversion predictions.
    3. Review and export results as CSV or JSON for further analysis.
    """,
    unsafe_allow_html=True,
)

# Horizontal line
display_divider()


# ------------------ Data Input Section ---------------- #
# Select Data Input Method
st.markdown("## Select Data Input Method")

input_method = st.radio(
    "Choose how you want to provide data:",
    ("Manual Input", "Upload JSON", "Use Sample Data"),
    index=0,
    help="**Manual Input**: Enter data manually through input fields. \
    \n**Upload JSON**: Upload a JSON file with lead data. \
    \n**Use Sample Data**: Use pre-filled sample data for testing.",
)

if input_method == "Upload JSON":
    # Display a preview of the expected JSON format
    with st.expander("Preview expected JSON format"):
        st.code(json.dumps(sample_json[0], indent=4), language="json")

# Horizontal line
display_divider()

# Ensure data_to_send is initialized
data_to_send = None

if input_method == "Upload JSON":

    # File uploader for JSON input
    uploaded_file = st.file_uploader("Choose a JSON file", type="json")

    if uploaded_file is not None:
        try:
            # Read and parse the JSON file
            data = json.load(uploaded_file)

            # Prepare and validate the input data
            data_to_send, error = process_validate_input_data(data)

            if error:
                st.error(error)
            else:
                st.success("JSON data loaded successfully!")

                # Display the data for API request
                with st.expander("Preview data to be sent to API"):
                    st.write(data_to_send)

        except json.JSONDecodeError:
            st.error("Invalid JSON file. Please upload a valid JSON file.")

elif input_method == "Use Sample Data":

    # Use sample JSON data directly
    data = sample_json

    # Prepare and validate the input data
    data_to_send, error = process_validate_input_data(data)

    if error:
        st.error(error)
    else:
        st.success("Sample data loaded successfully!")

        # Display the data for API request
        with st.expander("Preview data to be sent to API"):
            st.write(data_to_send)

elif input_method == "Manual Input":

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

    # Prepare data for API request
    data = [
        {
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
    ]

    # Prepare and validate the input data
    data_to_send, error = process_validate_input_data(data)

    if error:
        st.error(error)
    else:
        # Display the data for API request
        with st.expander("Preview data to be sent to API"):
            st.write(data_to_send)


# ------------------ Prediction Section ----------------- #
# Prediction Button
predict = st.button("Predict")

if predict:
    if data_to_send is None:
        # Map input methods to appropriate messages
        input_messages = {
            "Upload JSON": "Please upload a valid JSON file.",
            "Use Sample Data": "There was an issue loading the sample data.",
            "Manual Input": "Please complete the form with valid data.",
        }

        # Display the appropriate message based on selected input method
        st.info(input_messages[input_method])
    else:
        # Make a prediction request to the API
        success, prediction, probability, error = make_prediction_request(
            data_to_send, FASTAPI_URL
        )

        if not success:
            st.error(error)
        elif prediction is None or probability is None:
            st.error("API response missing required data.")
        else:
            st.success("Prediction successful!")

            if len(prediction) == 1:
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

            else:
                # Display distribution of predictions
                prediction_series = pd.Series(prediction)
                value_counts = prediction_series.value_counts().to_dict()

                # Total number of predictions
                total_count = len(prediction)

                # Get counts for each class (0 and 1)
                count_0 = value_counts.get(0, 0)  # Default value is 0
                count_1 = value_counts.get(1, 0)  # Default value is 0
                total = count_0 + count_1

                # Calculate percentages (handle division by zero)
                percentage_0 = (count_0 / total * 100) if total > 0 else 0
                percentage_1 = (count_1 / total * 100) if total > 0 else 0

                st.markdown(
                    f"""
                    <div class="custom-card">
                        <div class="custom-title">Distribution of Predictions</div>
                        <div class="custom-subtitle">Leads are likely to:</div>
                        <div style="display: flex; justify-content: center; gap: 100px;">
                            <div style="text-align: center;">
                                <span class="not-convert">NOT CONVERT</span>
                                <div style="font-size: 24px; margin-top: 10px;">
                                    {count_0} ({percentage_0:.1f}%)
                                </div>
                            </div>
                            <div style="text-align: center;">
                                <span class="convert">CONVERT</span>
                                <div style="font-size: 24px; margin-top: 10px;">
                                    {count_1} ({percentage_1:.1f}%)
                                </div>
                            </div>
                        </div>
                        <br>
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
            results_df, error = combine_data(data_to_send, prediction, probability)

            if error:
                st.error(error)
            else:
                # Only proceed if data was combined successfully
                with st.expander("See prediction output and associated probability"):
                    st.write(results_df.loc[:, ["prediction", "probability"]])

                # Export data to CSV or JSON
                csv_data, json_data, error = export_data(results_df)

                if error:
                    st.error(error)
                else:
                    display_export_buttons(csv_data, json_data)


# ------------------ Footer Section -------------------- #
# Back to Top Button
display_back_to_top()

# Horizontal line
display_divider()

# Footer with copyright and timestamp
display_footer()

# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
