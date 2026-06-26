import pandas as pd

df = pd.read_csv("data/jobs_raw.csv")
print(f"Raw jobs: {len(df)}")

df = df[[
    "job_id", "job_title", "employer_name",
    "job_city", "job_state", "job_country",
    "job_employment_type", "job_is_remote",
    "job_posted_at", "job_min_salary",
    "job_max_salary", "job_salary_period",
    "job_description", "job_apply_link"
]]

df["job_is_remote"] = df["job_is_remote"].fillna(False)
df["avg_salary"] = (df["job_min_salary"] + df["job_max_salary"]) / 2

# ── Full Skills List ──────────────────────────────────
skills_list = [
    # AI & GenAI (Hottest in 2026)
    "Generative AI", "GenAI", "Agentic AI", "AI Agents",
    "Prompt Engineering", "Large Language Models", "LLMs",
    "Retrieval-Augmented Generation", "RAG", "AI Automation",
    "Machine Learning", "Deep Learning", "MLOps",

    # Data
    "Data Science", "Data Engineering", "Data Analytics",
    "Power BI", "Tableau", "Apache Spark", "Apache Kafka",
    "TensorFlow", "PyTorch", "Pandas", "NumPy",

    # Programming
    "Python", "Java", "JavaScript", "TypeScript",
    "SQL", "C++", "C#", "Go", "Kotlin",

    # Web & Backend
    "React", "Node.js", "Spring Boot", "FastAPI",
    "Django", "Flask", "Next.js", "Angular",
    "REST APIs", "GraphQL", "Microservices",

    # Cloud & DevOps
    "AWS", "Azure", "GCP", "Google Cloud",
    "Cloud Computing", "Docker", "Kubernetes",
    "CI/CD", "Terraform", "Jenkins", "Ansible",
    "DevOps", "Git", "GitHub",

    # Databases
    "MySQL", "PostgreSQL", "MongoDB",
    "Redis", "Cassandra", "SQL Server",

    # Security
    "Cybersecurity", "Network Security",
    "Cloud Security", "Ethical Hacking",

    # Emerging Tech
    "Blockchain", "IoT", "Internet of Things",
    "Edge Computing",

    # CS Fundamentals
    "Data Structures", "Algorithms", "DSA",
    "System Design", "OOP", "Microservices",

    # Mobile
    "Flutter", "React Native", "Android", "iOS",

    # Testing
    "Selenium", "Cypress", "API Testing",

    # Soft Skills
    "Problem Solving", "Communication",
    "Leadership", "Business Analysis"
]

def extract_skills(description):
    if pd.isna(description):
        return ""
    return ", ".join([
        s for s in skills_list
        if s.lower() in description.lower()
    ])

df["skills"] = df["job_description"].apply(extract_skills)
df = df.drop(columns=["job_description"])

# Save
df.to_csv("cleaned_jobs.csv", index=False)
print(f"✅ Cleaned jobs: {len(df)}")
print(f"Cities: {df['job_city'].nunique()}")
print(f"Companies: {df['employer_name'].nunique()}")
print(f"\nSample skills extracted:")
print(df["skills"].head(5).to_string())
