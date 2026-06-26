import pandas as pd
from collections import Counter

# Load cleaned data
df = pd.read_csv("data/cleaned_jobs.csv")

print("="*50)
print("1. TOP HIRING COMPANIES")
print("="*50)
top_companies = df["employer_name"].value_counts().head(10)
print(top_companies.to_string())

print("\n")
print("="*50)
print("2. JOBS BY CITY")
print("="*50)
top_cities = df["job_city"].value_counts().head(10)
print(top_cities.to_string())

print("\n")
print("="*50)
print("3. REMOTE VS ON-SITE")
print("="*50)
remote_counts = df["job_is_remote"].value_counts()
print(remote_counts.to_string())

print("\n")
print("="*50)
print("4. TOP IN-DEMAND SKILLS")
print("="*50)
all_skills = []
for skills in df["skills"].dropna():
    if skills:
        all_skills.extend([s.strip() for s in skills.split(",")])
skill_counts = Counter(all_skills)
for skill, count in skill_counts.most_common(15):
    bar = "█" * count
    print(f"{skill:<25} {bar} ({count})")

print("\n")
print("="*50)
print("5. EMPLOYMENT TYPE")
print("="*50)
print(df["job_employment_type"].value_counts().to_string())

print("\n")
print("="*50)
print("6. JOBS BY STATE")
print("="*50)
print(df["job_state"].value_counts().head(10).to_string())