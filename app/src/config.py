# -------------------------------------------------------------------------- #
# Title: Pydantic Model for Request Body
# Description: Definition of Pydantic model for request body
# Author: Thomas Moesl
# Date: March 2025
# -------------------------------------------------------------------------- #


# ------------------ Import Libraries ------------------ #
# Import the required libraries
from pydantic import BaseModel, Field


# ------------------ Pydantic Model --------------------- #
# Define Pydantic model for request body
class PredictRequest(BaseModel):
    """
    Pydantic model for request body.

    Validates and structures input data for lead prediction with the following features:
        - Basic demographic: age
        - Website behavior: visits, time spent, page views
        - Occupation status: student, unemployed
        - Website interaction: first visit, profile completion
        - Activity channels: phone, website
        - Marketing channels: print media, digital media, educational, referral

    All numeric fields must be non-negative, and age must be between 0-100 years.

    Args:
        BaseModel: Base class for Pydantic models
    """

    # Define fields with validation rules
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
