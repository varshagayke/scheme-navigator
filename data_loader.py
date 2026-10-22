import pandas as pd
import streamlit as st

DATA_PATH = "data/government_scheme_navigator_2026_rag_dataset.csv"

# The CSV has 53 messy category names. We group them into a few clean ones.
CATEGORY_GROUPS = {
    "Education": "Education",
    "Agriculture": "Agriculture & Allied",
    "Animal Husbandry": "Agriculture & Allied",
    "Fisheries": "Agriculture & Allied",
    "Food Processing": "Agriculture & Allied",
    "Business": "Business & Startup",
    "Startup": "Business & Startup",
    "Health": "Health & Nutrition",
    "Nutrition": "Health & Nutrition",
    "Sanitation": "Health & Nutrition",
    "Skills": "Skills & Employment",
    "Employment": "Skills & Employment",
    "Youth": "Skills & Employment",
    "Livelihoods": "Skills & Employment",
    "Rural Livelihood": "Skills & Employment",
    "Urban Livelihood": "Skills & Employment",
    "Women": "Women & Child",
    "Women & Child": "Women & Child",
    "Women Welfare": "Women & Child",
    "Child Welfare": "Women & Child",
    "Social Security": "Pension, Savings & Insurance",
    "Pension": "Pension, Savings & Insurance",
    "Savings": "Pension, Savings & Insurance",
    "Insurance": "Pension, Savings & Insurance",
    "Banking": "Pension, Savings & Insurance",
    "Financial Inclusion": "Pension, Savings & Insurance",
    "Housing": "Housing & Infrastructure",
    "Energy": "Housing & Infrastructure",
    "Water": "Housing & Infrastructure",
    "Utility": "Housing & Infrastructure",
    "Environment": "Housing & Infrastructure",
    "Urban Infrastructure": "Housing & Infrastructure",
    "Rural Infrastructure": "Housing & Infrastructure",
    "Social Infrastructure": "Housing & Infrastructure",
    "Rural": "Housing & Infrastructure",
    "Tribal Welfare": "Social Welfare",
    "Tribal Livelihood": "Social Welfare",
    "Disability Welfare": "Social Welfare",
    "Disability Inclusion": "Social Welfare",
    "Disability Services": "Social Welfare",
    "Senior Citizens": "Social Welfare",
    "Senior Citizen Welfare": "Social Welfare",
    "Social Welfare": "Social Welfare",
    "Social Assistance": "Social Welfare",
    "Social Justice": "Social Welfare",
    "Minority": "Social Welfare",
    "Worker Welfare": "Social Welfare",
    "Food Security": "Social Welfare",
}


def load_schemes(path=DATA_PATH):
    df = pd.read_csv(path)

    # 1. Clean category: take the text before the first "/", then map to a group
    first_part = df["category"].str.split("/").str[0].str.strip()
    df["category_group"] = first_part.map(CATEGORY_GROUPS).fillna("Other")

    # 2. Empty age means "no limit", so fill with 0 and 120
    df["min_age"] = df["min_age"].fillna(0)
    df["max_age"] = df["max_age"].fillna(120)

    # 3. Simple level label for the filter
    is_state = df["government_level"].str.contains("State", regex=False) & \
        ~df["government_level"].str.contains("Central", regex=False)
    df["level_group"] = is_state.map({True: "Maharashtra State", False: "Central"})

    # 4. One text column that we search in (we will reuse this idea for RAG later)
    df["search_text"] = (
        df["scheme_name"] + " " + df["scheme_description"] + " " +
        df["target_beneficiary"] + " " + df["benefit"] + " " +
        df["occupation_or_profile"]
    ).str.lower()

    return df


@st.cache_data
def get_schemes():
    """Load and clean the CSV once, then reuse it on every page."""
    return load_schemes()
