# -------------------------------------------------------------------------- #
# Title: Style Configuration for Streamlit App
# Description: This file contains style configurations for the Streamlit app.
# Author: Thomas Moesl
# Date: February 2025
# -------------------------------------------------------------------------- #


# ------------------ Import Libraries ------------------ #
# Import the required libraries
import streamlit as st
import datetime


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
            border: none;
            border-top: 1px solid var(--primary-color);
            opacity: 0.3;
            margin: 1.5rem 0;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# Function to display a horizontal divider
def display_divider():
    """Display a themed horizontal divider."""
    st.markdown(
        f"<hr style='border: 1px solid {line_color};'>",
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


# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
