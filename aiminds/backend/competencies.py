"""Competency framework + gap analysis. Extend COMPETENCIES with your own questions."""
COMPETENCIES = {
    "samp": {"name": "Survey design & sampling", "questions": [
        {"q": "Every unit has a known, non-zero chance of selection. This is:",
         "options": ["Probability sampling", "Quota sampling", "Purposive sampling", "Snowball sampling"], "answer": 0},
        {"q": "Splitting a population into homogeneous groups before sampling is:",
         "options": ["Cluster sampling", "Stratified sampling", "Systematic sampling", "Convenience sampling"], "answer": 1}]},
    "na": {"name": "National accounts", "questions": [
        {"q": "GDP at market prices equals GVA plus:",
         "options": ["Product taxes minus product subsidies", "Product subsidies minus product taxes", "Only direct taxes", "Net factor income"], "answer": 0},
        {"q": "Real GDP differs from nominal GDP because it:",
         "options": ["Excludes services", "Adjusts for price changes", "Excludes imports", "Uses calendar year"], "answer": 1}]},
    "gov": {"name": "Data governance & ethics", "questions": [
        {"q": "Before publishing microdata you should apply:",
         "options": ["More columns", "Disclosure control", "Metadata deletion", "Nothing"], "answer": 1},
        {"q": "Metadata mainly helps users to:",
         "options": ["Understand definitions and methods", "Speed up servers", "Replace data", "Hide sources"], "answer": 0}]},
    "qual": {"name": "Data collection & quality", "questions": [
        {"q": "Non-response bias arises when:",
         "options": ["The sample is too large", "Respondents differ systematically from non-respondents", "Questions are too short", "Data is entered twice"], "answer": 1},
        {"q": "Which check catches an impossible value such as age 250?",
         "options": ["Range validation", "Weighting", "Imputation", "Stratification"], "answer": 0}]},
    "an": {"name": "Statistical analysis", "questions": [
        {"q": "A median is preferred over the mean when data is:",
         "options": ["Normally distributed", "Heavily skewed with outliers", "Perfectly symmetric", "Purely categorical"], "answer": 1},
        {"q": "A 95% confidence interval means:",
         "options": ["95% of data lies inside it", "The method captures the true value in 95% of repeated samples", "The p-value is 0.95", "The estimate is 95% accurate"], "answer": 1}]},
    "viz": {"name": "Data visualisation", "questions": [
        {"q": "Best chart for a trend over time:",
         "options": ["Pie chart", "Line chart", "Word cloud", "Donut chart"], "answer": 1},
        {"q": "Starting a bar chart axis above zero mainly:",
         "options": ["Improves accuracy", "Exaggerates differences", "Reduces file size", "Has no effect"], "answer": 1}]},
}

# Display order shown in the UI
COMPETENCIES = {k: COMPETENCIES[k] for k in ["samp", "qual", "na", "an", "viz", "gov"]}

def analyse(answers: dict[str, list[int]]) -> list[dict]:
    """answers: {comp_id: [chosen option index per question]} -> per-competency score and level."""
    report = []
    for cid, comp in COMPETENCIES.items():
        chosen = answers.get(cid, [])
        correct = sum(1 for i, q in enumerate(comp["questions"]) if i < len(chosen) and chosen[i] == q["answer"])
        total = len(comp["questions"])
        ratio = correct / total
        level = "strong" if ratio == 1 else "developing" if ratio >= 0.5 else "gap"
        report.append({"id": cid, "name": comp["name"], "correct": correct, "total": total, "level": level})
    return report
