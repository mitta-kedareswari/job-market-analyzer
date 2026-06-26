import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import requests
import os
from datetime import datetime, timedelta
import time

# ── Page Config ──────────────────────────────────────
st.set_page_config(
    page_title="India Job Market Analyzer",
    page_icon="📊",
    layout="wide"
)

# ── Skills List ───────────────────────────────────────
skills_list = [
    # Programming Languages
    "Python", "Java", "JavaScript", "TypeScript", "C++", "C#",
    "Go", "Rust", "Kotlin", "Swift", "SQL",
    # CS Fundamentals
    "Data Structures", "Algorithms", "DSA", "OOP",
    "Operating Systems", "DBMS", "Computer Networks", "System Design",
    # Web Development
    "HTML", "CSS", "React", "Angular", "Vue.js", "Node.js",
    "Express.js", "Next.js",
    # Mobile Development
    "Android", "iOS", "Flutter", "React Native",
    # Backend Development
    "Spring Boot", ".NET", "Django", "Flask", "FastAPI", "Laravel",
    # Databases
    "MySQL", "PostgreSQL", "Oracle Database", "SQL Server",
    "MongoDB", "Redis", "Cassandra",
    # Cloud Computing
    "AWS", "Azure", "GCP", "Google Cloud",
    # DevOps
    "Git", "GitHub", "Docker", "Kubernetes", "Jenkins",
    "Terraform", "Ansible", "CI/CD",
    # AI & Data
    "Machine Learning", "Deep Learning", "Generative AI",
    "Prompt Engineering", "NLP", "Computer Vision",
    "Data Analytics", "Data Engineering", "Data Science",
    "Big Data", "TensorFlow", "PyTorch", "Power BI", "Tableau",
    "Apache Spark", "Apache Kafka", "Pandas", "NumPy",
    # Cybersecurity
    "Network Security", "Ethical Hacking", "Penetration Testing",
    "SOC Operations", "SIEM", "Cloud Security",
    # Testing & QA
    "Selenium", "Cypress", "Playwright", "JUnit", "TestNG",
    "API Testing",
    # APIs & Architecture
    "REST APIs", "GraphQL", "Microservices",
    "Event-Driven Architecture",
    # Soft Skills
    "Problem Solving", "Critical Thinking", "Communication",
    "Collaboration", "Leadership", "Time Management",
    "Adaptability", "Business Analysis"
]

# ── Auto Refresh Function ─────────────────────────────
API_KEY = "your_api_key_here"  # paste your key

def fetch_fresh_jobs():
    url = "https://jsearch.p.rapidapi.com/search-v2"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    companies = [
        "TCS", "Infosys", "Wipro", "HCLTech", "Tech Mahindra",
        "Accenture", "Cognizant", "Capgemini", "IBM", "Deloitte",
        "PwC", "EY", "KPMG", "LTIMindtree", "Oracle",
        "Microsoft", "Google", "Amazon", "Salesforce", "Adobe"
    ]

    cities = [
        "Bengaluru", "Hyderabad", "Pune", "Chennai",
        "Gurugram", "Noida", "Mumbai", "Kochi",
        "Ahmedabad", "Kolkata"
    ]

    roles = [
        "Software Engineer", "Full Stack Developer",
        "Backend Developer", "Frontend Developer",
        "Java Developer", "Python Developer",
        "AI Engineer", "Machine Learning Engineer",
        "Data Scientist", "Data Analyst",
        "Associate Software Engineer", "Junior Data Analyst",
        "Trainee Software Engineer", "Junior Python Developer"
    ]

    all_jobs = []
    total = 0
    MAX = 50  # Limited during auto refresh to save API calls

    for role in roles:
        for company in companies:
            if total >= MAX:
                break
            params = {
                "query": f"{role} at {company} India",
                "num_pages": "1",
                "country": "in",
                "language": "en"
            }
            try:
                response = requests.get(url, headers=headers, params=params)
                data = response.json()
                if "data" in data and "jobs" in data["data"]:
                    jobs = data["data"]["jobs"]
                    filtered = [j for j in jobs if j.get("job_city") in cities]
                    all_jobs.extend(filtered)
                total += 1
                time.sleep(0.5)
            except:
                pass
        if total >= MAX:
            break
    return all_jobs

def clean_jobs(all_jobs):
    df = pd.DataFrame(all_jobs)
    cols = [c for c in [
        "job_id", "job_title", "employer_name",
        "job_city", "job_state", "job_country",
        "job_employment_type", "job_is_remote",
        "job_posted_at", "job_min_salary",
        "job_max_salary", "job_salary_period",
        "job_description", "job_apply_link"
    ] if c in df.columns]
    df = df[cols]
    df["job_is_remote"] = df["job_is_remote"].fillna(False)
    df["avg_salary"] = (
        df.get("job_min_salary", 0) + df.get("job_max_salary", 0)
    ) / 2

    def extract_skills(description):
        if pd.isna(description):
            return ""
        return ", ".join([
            s for s in skills_list
            if s.lower() in description.lower()
        ])

    df["skills"] = df["job_description"].apply(extract_skills)
    df = df.drop(columns=["job_description"], errors="ignore")
    return df

def check_and_refresh():
    last_fetch_file = "last_fetch.txt"
    should_refresh = True

    if os.path.exists(last_fetch_file):
        with open(last_fetch_file, "r") as f:
            last_fetch = datetime.fromisoformat(f.read().strip())
        if datetime.now() - last_fetch < timedelta(hours=24):
            should_refresh = False

    if should_refresh:
        with st.spinner("🔄 Fetching fresh job data... please wait"):
            jobs = fetch_fresh_jobs()
            if jobs:
                df = clean_jobs(jobs)
                df = df.drop_duplicates(subset=["job_id"]) if "job_id" in df.columns else df
                df.to_csv("cleaned_jobs.csv", index=False)
                with open(last_fetch_file, "w") as f:
                    f.write(datetime.now().isoformat())
                st.success(f"✅ Data refreshed! {len(df)} fresh jobs loaded.")
            else:
                st.warning("⚠️ Could not fetch fresh data. Using existing data.")

# ── Check and Refresh ─────────────────────────────────
check_and_refresh()

# ── Load Data ─────────────────────────────────────────
df = pd.read_csv("cleaned_jobs.csv")

# Last updated
if os.path.exists("last_fetch.txt"):
    with open("last_fetch.txt", "r") as f:
        last_fetch = datetime.fromisoformat(f.read().strip())
    st.caption(f"🕒 Last updated: {last_fetch.strftime('%d %b %Y, %I:%M %p')}")

# ── Title ─────────────────────────────────────────────
st.title("📊 India Job Market Trend Analyzer")
st.markdown("**Real-time insights from top companies across major Indian cities**")
st.divider()

# ── Top Metrics ───────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Jobs", len(df))
col2.metric("Cities", df["job_city"].nunique())
col3.metric("Companies", df["employer_name"].nunique())
col4.metric("Remote Jobs", int(df["job_is_remote"].sum()))

st.divider()

# ── Sidebar Filters ───────────────────────────────────
st.sidebar.title("🔎 Filters")

city_filter = st.sidebar.multiselect(
    "🏙️ Select Cities",
    options=sorted(df["job_city"].dropna().unique().tolist()),
    default=[]
)

company_filter = st.sidebar.multiselect(
    "🏢 Select Companies",
    options=sorted(df["employer_name"].dropna().unique().tolist()),
    default=[]
)

remote_filter = st.sidebar.selectbox(
    "🏠 Job Type",
    ["All", "Remote", "On-Site"]
)

# Apply filters
filtered = df.copy()
if city_filter:
    filtered = filtered[filtered["job_city"].isin(city_filter)]
if company_filter:
    filtered = filtered[filtered["employer_name"].isin(company_filter)]
if remote_filter == "Remote":
    filtered = filtered[filtered["job_is_remote"] == True]
elif remote_filter == "On-Site":
    filtered = filtered[filtered["job_is_remote"] == False]

st.sidebar.markdown(f"**Showing {len(filtered)} of {len(df)} jobs**")

# ── Row 1: Cities + Companies ─────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏙️ Top Cities Hiring")
    city_data = filtered["job_city"].value_counts().head(10).reset_index()
    city_data.columns = ["City", "Jobs"]
    fig = px.bar(city_data, x="Jobs", y="City",
                 orientation="h", color="Jobs",
                 color_continuous_scale="Blues")
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🏢 Top Hiring Companies")
    company_data = filtered["employer_name"].value_counts().head(10).reset_index()
    company_data.columns = ["Company", "Jobs"]
    fig = px.bar(company_data, x="Jobs", y="Company",
                 orientation="h", color="Jobs",
                 color_continuous_scale="Greens")
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ── Row 2: Skills + Remote ────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔥 Top In-Demand Skills")
    all_skills = []
    for skills in filtered["skills"].dropna():
        if skills:
            all_skills.extend([s.strip() for s in skills.split(",")])
    skill_counts = Counter(all_skills).most_common(15)
    skill_df = pd.DataFrame(skill_counts, columns=["Skill", "Count"])
    fig = px.bar(skill_df, x="Count", y="Skill",
                 orientation="h", color="Count",
                 color_continuous_scale="Reds")
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🏠 Remote vs On-Site")
    remote_df = filtered["job_is_remote"].map({True: "Remote", False: "On-Site"})
    remote_counts = remote_df.value_counts().reset_index()
    remote_counts.columns = ["Type", "Count"]
    fig = px.pie(remote_counts, names="Type", values="Count",
                 color_discrete_sequence=["#636EFA", "#EF553B"])
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ── Row 3: State wise jobs ────────────────────────────
st.subheader("🗺️ Jobs by State")
state_data = filtered["job_state"].value_counts().reset_index()
state_data.columns = ["State", "Jobs"]
fig = px.bar(state_data, x="State", y="Jobs",
             color="Jobs", color_continuous_scale="Purples")
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ── Job Listings Table ────────────────────────────────
st.subheader("📋 All Job Listings")
st.dataframe(
    filtered[["job_title", "employer_name", "job_city",
              "job_state", "job_is_remote", "skills"]],
    use_container_width=True
)
st.caption(f"Showing {len(filtered)} of {len(df)} jobs")

st.divider()

# ── Manual Refresh Button ─────────────────────────────
if st.button("🔄 Force Refresh Data Now"):
    if os.path.exists("last_fetch.txt"):
        os.remove("last_fetch.txt")
    st.rerun()

st.divider()

# ── Skill Gap Analyzer ────────────────────────────────
st.subheader("🔍 Skill Gap Analyzer")
st.markdown("**Enter your skills and see how you match the job market!**")

user_input = st.text_input(
    "Type your skills separated by commas:",
    placeholder="e.g. Python, SQL, React, Docker"
)

if user_input:
    user_skills = [s.strip().lower() for s in user_input.split(",") if s.strip()]
    all_skills = []
    for skills in filtered["skills"].dropna():
        if skills:
            all_skills.extend([s.strip() for s in skills.split(",")])
    top_skills = [s for s, _ in Counter(all_skills).most_common(15)]

    matched = [s for s in top_skills if s.lower() in user_skills]
    missing = [s for s in top_skills if s.lower() not in user_skills]
    score = int((len(matched) / len(top_skills)) * 100) if top_skills else 0

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    col1.metric("Your Match Score", f"{score}%")
    col2.metric("✅ Skills You Have", len(matched))
    col3.metric("❌ Skills Missing", len(missing))

    st.markdown("### 📊 Your Market Readiness")
    st.progress(score / 100)

    if score >= 70:
        st.success("🔥 Excellent! You are highly marketable!")
    elif score >= 40:
        st.warning("💪 Good start! Learn a few more skills to stand out.")
    else:
        st.error("📚 Keep learning! Focus on the missing skills below.")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✅ Skills You Have")
        if matched:
            for skill in matched:
                st.success(f"✅ {skill}")
        else:
            st.info("None matched yet — keep learning!")

    with col2:
        st.markdown("### ❌ Skills to Learn")
        if missing:
            for skill in missing:
                st.error(f"❌ {skill}")
        else:
            st.balloons()
            st.success("🎉 You have all top skills!")

    st.markdown("---")
    st.markdown("### 📚 Free Resources to Learn Missing Skills")
    resources = {
        "Python": "https://www.learnpython.org",
        "SQL": "https://www.sqltutorial.org",
        "Java": "https://www.learnjavaonline.org",
        "JavaScript": "https://javascript.info",
        "React": "https://react.dev/learn",
        "Docker": "https://docs.docker.com/get-started",
        "Kubernetes": "https://kubernetes.io/docs/tutorials",
        "AWS": "https://aws.amazon.com/training/free",
        "Azure": "https://learn.microsoft.com/en-us/azure",
        "Machine Learning": "https://www.coursera.org/learn/machine-learning",
        "Deep Learning": "https://www.deeplearning.ai",
        "Power BI": "https://learn.microsoft.com/en-us/power-bi",
        "Tableau": "https://www.tableau.com/learn/training",
        "Git": "https://learngitbranching.js.org",
        "MongoDB": "https://learn.mongodb.com",
        "PostgreSQL": "https://www.postgresqltutorial.com",
        "TypeScript": "https://www.typescriptlang.org/docs",
        "Node.js": "https://nodejs.org/en/learn",
        "Spring Boot": "https://spring.io/guides",
        "Flutter": "https://flutter.dev/learn"
    }
    for skill in missing[:5]:
        if skill in resources:
            st.markdown(f"- **{skill}** → [Free Course]({resources[skill]})")

st.divider()

# ── Job Recommender ───────────────────────────────────
st.subheader("🎯 Job Recommender")
st.markdown("**Find jobs that match your skills!**")

recommend_input = st.text_input(
    "Enter your skills to find matching jobs:",
    placeholder="e.g. Python, SQL, Power BI",
    key="recommend_input"
)

if recommend_input:
    user_skills = [s.strip().lower() for s in recommend_input.split(",") if s.strip()]

    def calculate_match(job_skills):
        if pd.isna(job_skills) or job_skills == "":
            return 0
        job_skill_list = [s.strip().lower() for s in job_skills.split(",")]
        if not job_skill_list:
            return 0
        matched = sum(1 for s in job_skill_list if s in user_skills)
        return int((matched / len(job_skill_list)) * 100)

    filtered["match_%"] = filtered["skills"].apply(calculate_match)
    recommended = filtered[filtered["match_%"] > 0].sort_values(
        "match_%", ascending=False
    ).head(10)

    if len(recommended) == 0:
        st.warning("⚠️ No matching jobs found. Try adding more skills!")
    else:
        st.success(f"🎉 Found {len(recommended)} matching jobs for you!")
        st.markdown("---")

        for i, row in recommended.iterrows():
            match = row["match_%"]
            color = "🟢" if match >= 70 else "🟡" if match >= 40 else "🔴"

            with st.expander(
                f"{color} {match}% Match — {row['job_title']} at {row['employer_name']}"
            ):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**🏢 Company:** {row['employer_name']}")
                    st.markdown(f"**📍 Location:** {row['job_city']}, {row['job_state']}")
                    st.markdown(f"**💼 Type:** {row['job_employment_type']}")
                    st.markdown(f"**🏠 Remote:** {'Yes' if row['job_is_remote'] else 'No'}")
                with col2:
                    st.markdown(f"**🛠️ Required Skills:** {row['skills']}")
                    st.progress(match / 100)
                    st.markdown(f"**Match Score: {match}%**")
