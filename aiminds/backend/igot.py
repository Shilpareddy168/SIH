"""iGOT Karmayogi integration layer. Keep all iGOT calls here so the rest of the app never changes.
Set IGOT_API_URL once you have official API access; until then sample data is returned."""
import os
import httpx

IGOT_URL = os.getenv("IGOT_API_URL")
SAMPLE = {
    "samp": ["Sampling Methods for Official Surveys", "Designing Household Surveys"],
    "na": ["Introduction to National Accounts", "GDP Estimation & Deflators"],
    "gov": ["Statistical Disclosure Control", "Metadata & Data Standards"],
    "qual": ["Data Quality Frameworks", "Field Data Collection & Validation"],
    "an": ["Applied Statistics for Officers", "Estimation & Confidence Intervals"],
    "viz": ["Communicating Data with Charts", "Dashboards for Policy Makers"],
}

def courses_for(competency_id: str) -> list[str]:
    if IGOT_URL:
        try:  # endpoint shape is an assumption; adapt to the real iGOT API docs
            return httpx.get(f"{IGOT_URL}/courses", params={"competency": competency_id}, timeout=5).json()
        except (httpx.HTTPError, ValueError):
            pass
    return SAMPLE.get(competency_id, [])
