"""Tools for processing LinkedIn profile data."""
from typing import Any, Dict


HIRABLE_FIELDS = {
    "email",
    "headline",
    "current_position",
    "about",
    "education",
    "professional_experience",
    "skills",
    "licenses_certifications",
}


def filter_hirable_profile_data(profile: Dict[str, Any]) -> Dict[str, Any]:
    """Return only fields relevant to hiring."""
    return {key: value for key, value in profile.items() if key in HIRABLE_FIELDS}
