"""Rule-based eligibility engine. Plain Python, no AI.
The AI will only explain results later. These rules decide who qualifies."""

# words that tell us a scheme is meant for a type of person
OCCUPATION_WORDS = {
    "Farmer": ["farmer", "agricultur", "livestock", "fish", "kisan"],
    "Student": ["student", "scholar", "education"],
    "Woman": ["woman", "women", "girl", "widow", "mahila"],
    "Senior Citizen": ["senior", "elderly", "old age", "pension"],
    "Person with Disability": ["disab", "divyang"],
    "Entrepreneur / Business": ["entrepreneur", "msme", "startup", "business", "trader"],
    "Job Seeker / Youth": ["job", "youth", "skill", "unemployed", "employment"],
    "Worker / Labourer": ["worker", "labour", "labor"],
    "Other": [],
}

# words that tell us a scheme is open to everyone
GENERAL_WORDS = ["household", "individual", "citizen", "resident", "people", "family"]


def check_scheme(row, person):
    """Return (result, reasons) for one scheme.
    result is 'no', 'best' or 'general'."""
    reasons = []

    # ---- HARD RULES: if any fails, the person is NOT eligible ----
    age = person["age"]
    if not (row["min_age"] <= age <= row["max_age"]):
        return "no", []
    if row["min_age"] > 0 or row["max_age"] < 120:
        reasons.append(f"Your age {age} is within {int(row['min_age'])}-{int(row['max_age'])}")

    if person["gender"] == "Male" and row["gender"] == "Female":
        return "no", []

    if person["area"] == "Rural" and row["residence"] == "Urban":
        return "no", []
    if person["area"] == "Urban" and row["residence"] == "Rural":
        return "no", []

    if not person["maharashtra"] and row["level_group"] == "Maharashtra State":
        return "no", []

    # ---- SOFT RULE: does the scheme match the person's occupation? ----
    profile_text = (row["occupation_or_profile"] + " " + row["target_beneficiary"]).lower()
    words = OCCUPATION_WORDS[person["occupation"]]
    if any(w in profile_text for w in words):
        reasons.append(f"Made for: {person['occupation']}")
        if person["gender"] == "Female" and row["gender"] in ("Female", "Female/All", "All/Female"):
            reasons.append("Has benefits for women")
        return "best", reasons

    if "all" in profile_text.split() or any(w in profile_text for w in GENERAL_WORDS):
        reasons.append("Open to general public")
        return "general", reasons

    return "no", []


def find_schemes(df, person):
    """Run check_scheme on every row and return best matches and general ones."""
    best, general = [], []
    for _, row in df.iterrows():
        result, reasons = check_scheme(row, person)
        if result == "best":
            best.append((row, reasons))
        elif result == "general":
            general.append((row, reasons))
    return best, general
