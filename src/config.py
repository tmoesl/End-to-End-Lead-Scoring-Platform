# ---------------------- Configuration File -------------------------------- #
# Author: Thomas Moesl
# Date: February 2025
# Description: Definition of Pydantic model for request body
# -------------------------------------------------------------------------- #

# ---------------- Import Libraries ---------------- #
# Import the required libraries
from pydantic import BaseModel, Field


# ---------------- Pydantic Model ------------------ #
# Define Pydantic model for request body
class PredictRequest(BaseModel):
    age: int = Field(ge=0, le=100)
    website_visits: int = Field(ge=0)
    time_spent_on_website: float = Field(ge=0)
    page_views_per_visit: float = Field(ge=0)
    current_occupation_student: bool
    current_occupation_unemployed: bool
    first_interaction_website: bool
    profile_completed_low: bool
    profile_completed_medium: bool
    last_activity_phone: bool
    last_activity_website: bool
    print_media_type1_yes: bool
    print_media_type2_yes: bool
    digital_media_yes: bool
    educational_channels_yes: bool
    referral_yes: bool


# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
