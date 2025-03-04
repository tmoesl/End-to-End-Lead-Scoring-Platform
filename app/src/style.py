# -------------------------------------------------------------------------- #
# Title: Style Configuration for Streamlit App
# Description: This file contains style configurations for the Streamlit app.
# Author: Thomas Moesl
# Date: March 2025
# -------------------------------------------------------------------------- #


# ------------------ Import Libraries ------------------ #
# Import the required libraries
import datetime

import streamlit as st

# ---------------- Style Configuration ----------------- #
# Define style configuration
STYLE_CONFIG = {
    "CONVERT_COLOR": "#008F4C",  # Bright green that works on both modes
    "NOT_CONVERT_COLOR": "#FF4B4B",  # Coral red that works on both modes
    "CARD_BG": "#40444B",  # Slate blue that works well with text #2E2F38
    "BORDER_COLOR": "#FF914D",  # Medium gray for borders #4B5563
    "LINE_COLOR": "#FF914D",  # Use Streamlit's primary color for lines
}

# Extract style configuration
convert_color = STYLE_CONFIG["CONVERT_COLOR"]
not_convert_color = STYLE_CONFIG["NOT_CONVERT_COLOR"]
card_bg = STYLE_CONFIG["CARD_BG"]
border_color = STYLE_CONFIG["BORDER_COLOR"]
line_color = STYLE_CONFIG["LINE_COLOR"]


# ------------------ Style Functions ------------------ #
# Function to initialize page styling
def init_page_style():
    """Initialize page styling and CSS variables."""
    st.markdown(
        f"""
        <style>
        /* Import fonts */
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap');

        /* Base styles */
        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}
        
        /* Text sizing */
        h1 {{ font-size: 34px !important; }}
        h2 {{ font-size: 26px !important; }}
        h3 {{ font-size: 22px !important; }}
        p, li, div {{ font-size: 18px !important; }}

        /* Custom components */
        .custom-card {{
            color: var(--text-color);
            background-color: {card_bg};
            padding: 20px;
            border-radius: 10px;
            border: 1.5px solid {border_color} !important;
            text-align: center;
        }}

        .custom-title {{
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 15px;
        }}

        .custom-subtitle {{
            font-size: 24px;
            margin-bottom: 5px;
        }}

        .not-convert {{
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 25px;
            color: {not_convert_color};
        }}

        .convert {{
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 25px;
            color: {convert_color};
        }}

        .prediction-text {{
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 25px;
        }}
        
        .probability-text {{
            font-size: 24px;
            margin-top: 15px;
            margin-bottom: 5px;
        }}

        .custom-divider {{
            height: 2px;
            background: {line_color};
            opacity: 0.9;
            margin: 1.0rem 0;
            border-radius: 2px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# Function to initialize GitHub links styling
def init_github_links_style():
    """Initialize GitHub links styling."""
    st.markdown(
        f"""
        <style>
        .github-links {{
            text-align: left;
            margin-top: -5px;
            margin-bottom: -30px;
        }}
        .github-text {{
            font-size: 14px;
            font-style: italic;
            color: var(--text-color) !important;
        }}
        .github-link {{
            color: var(--text-color) !important;
            transition: opacity 0.4s;
        }}
        .github-link:hover {{
            opacity: 0.7;
            color: {line_color} !important;
        }}
        .github-separator {{
            color: var(--text-color);
            margin: 0 2px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# Function to display GitHub repository links
def display_github_links():
    """Display GitHub repository links."""
    st.markdown(
        """
        <div class="github-links">
            <span class="github-text">
                <strong>GitHub Repositories:</strong> 
                <a href="https://github.com/tmoesl/lead-conversion-prediction" 
                   target="_blank" 
                   class="github-link">Model Training & Evaluation</a>
                <span class="github-separator">|</span>
                <a href="https://github.com/tmoesl/lcp-aws-ec2" 
                   target="_blank" 
                   class="github-link">End-to-End Application Deployment</a>
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Function to display a 'Back to Top' link
def display_back_to_top():
    """Display a 'Back to Top' link. Identical formatting to display_github_links()."""
    st.markdown(
        """
        <div class="github-links" style="text-align: right;">
            <span class="github-text">
                <a href="#ml-model-lead-conversion-prediction" 
                   class="github-link">Get Back to Top</a>
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Function to display a horizontal divider
def display_divider():
    """Display a themed horizontal divider."""
    st.markdown(
        "<div class='custom-divider'></div>",
        unsafe_allow_html=True,
    )


# Function to display the footer
def display_footer():
    """Display the footer with copyright information."""

    current_year = datetime.datetime.now().year
    st.markdown(
        f"""
        <div style="text-align: center; font-size: small; color: gray;">
            &copy; {current_year} Thomas Moesl. All rights reserved.
        </div>
        """,
        unsafe_allow_html=True,
    )


# Function to display download buttons for CSV and JSON exports
def display_export_buttons(csv_data, json_data):
    """Display download buttons in the UI.

    Args:
        csv_data: The CSV data to export
        json_data: The JSON data to export

    Returns:
        None
    """
    if csv_data is None or json_data is None:
        st.error("No data available for export.")
        return

    # Create columns for buttons
    scol1, bcol1, scol2 = st.columns([1.6, 2.8, 1.6])

    with bcol1:  # This column holds both buttons together
        btn1_col, btn2_col = st.columns([1, 1])  # Equal spacing between buttons

    with btn1_col:
        st.download_button(
            label="Export to CSV",
            data=csv_data,
            file_name="predictions.csv",
            mime="text/csv",
        )

    with btn2_col:
        st.download_button(
            label="Export to JSON",
            data=json_data,
            file_name="predictions.json",
            mime="application/json",
        )


# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
