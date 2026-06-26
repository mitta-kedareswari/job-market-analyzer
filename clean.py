import pandas as pd

# Load raw data
df = pd.read_csv("data/jobs.csv")
print(f"Raw jobs: {len(df)}")

# ── 1. Keep only useful columns ──────────────────────
df = df[[
    "job_title",
    "employer_name",
    "job_city",
    "job_state",
    "job_country",
    "job_employment_type",
    "job_is_remote",
    "job_posted_at",
    "job_min_salary",
    "job_max_salary",
    "job_salary_period",
    "job_description"
]]

# ── 2. Clean job titles ──────────────────────────────
df["job_title"] = df["job_title"].str.strip()

# ── 3. Fix remote column ─────────────────────────────
df["job_is_remote"] = df["job_is_remote"].fillna(False)

# ── 4. Add average salary column ────────────────────
df["avg_salary"] = (df["job_min_salary"] + df["job_max_salary"]) / 2

# ── 5. Extract skills from job description ───────────
skills_list = [
    "Python", "SQL", "Excel", "Power BI", "Tableau",
    "Machine Learning", "R", "Spark", "AWS", "Azure",
    "Pandas", "NumPy", "TensorFlow", "Keras", "Statistics",
    "Data Visualization", "Deep Learning", "NLP"
]

def extract_skills(description):
    if pd.isna(description):
        return ""
    found = []
    for skill in skills_list:
        if skill.lower() in description.lower():
            found.append(skill)
    return ", ".join(found)

df["skills"] = df["job_description"].apply(extract_skills)

# ── 6. Drop description column (no longer needed) ───
df = df.drop(columns=["job_description"])

# ── 7. Save cleaned data ─────────────────────────────
df.to_csv("data/cleaned_jobs.csv", index=False)

print(f"Cleaned jobs: {len(df)}")
print("\nSample:")
print(df.head(3).to_string())
print("\nSkills found in first 5 jobs:")
print(df["skills"].head(5).to_string())