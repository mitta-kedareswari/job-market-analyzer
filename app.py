import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import requests
import os
import json
from datetime import datetime, timedelta

# ── Page Config ──────────────────────────────────────
st.set_page_config(
    page_title="Job Market Analyzer",
    page_icon="📊",
    layout="wide"
)

# ── Auto Refresh Function ─────────────────────────────
API_KEY = "b7ef8fee4bmsh4e9cd5799d84039p1baf55jsn9696df9564e1"  

def fetch_fresh_jobs():
    url = "https://jsearch.p.rapidapi.com/search-v2"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    queries = [
        "data analyst jobs in India",
        "data scientist jobs in India",
        "business analyst jobs in India",
        "python developer jobs in India",
        "machine learning engineer jobs in India"
    ]
    all_jobs = []
    for query in queries:
        params = {
            "query": query,
            "num_pages": "1",
            "country": "in",
            "language": "en"
        }
        try:
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            if "data" in data and "jobs" in data["data"]:
                all_jobs.extend(data["data"]["jobs"])
        except:
            pass
    return all_jobs

def clean_jobs(all_jobs):
    df = pd.DataFrame(all_jobs)
    df = df[[
        "job_title", "employer_name", "job_city",
        "job_state", "job_country", "job_employment_type",
        "job_is_remote", "job_posted_at",
        "job_min_salary", "job_max_salary",
        "job_salary_period", "job_description"
    ]]
    df["job_is_remote"] = df["job_is_remote"].fillna(False)
    df["avg_salary"] = (df["job_min_salary"] + df["job_max_salary"]) / 2

    skills_list = [
        "Python", "SQL", "Excel", "Power BI", "Tableau",
        "Machine Learning", "R", "Spark", "AWS", "Azure",
        "Pandas", "NumPy", "TensorFlow", "Keras", "Statistics",
        "Data Visualization", "Deep Learning", "NLP"
    ]

    def extract_skills(description):
        if pd.isna(description):
            return ""
        return ", ".join([s for s in skills_list if s.lower() in description.lower()])

    df["skills"] = df["job_description"].apply(extract_skills)
    df = df.drop(columns=["job_description"])
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
                df.to_csv("cleaned_jobs.csv", index=False)
                with open(last_fetch_file, "w") as f:
                    f.write(datetime.now().isoformat())
                st.success(f"✅ Data refreshed! {len(df)} fresh jobs loaded.")
            else:
                st.warning("⚠️ Could not fetch fresh data. Using existing data.")

# ── Check and Refresh Data ────────────────────────────
check_and_refresh()

# ── Load Data ─────────────────────────────────────────
df = pd.read_csv("cleaned_jobs.csv")

# Show last updated time
if os.path.exists("last_fetch.txt"):
    with open("last_fetch.txt", "r") as f:
        last_fetch = datetime.fromisoformat(f.read().strip())
    st.caption(f"🕒 Last updated: {last_fetch.strftime('%d %b %Y, %I:%M %p')}")

# ── Title ─────────────────────────────────────────────
st.title("📊 India Job Market Trend Analyzer")
st.markdown("**Real-time insights from live job postings**")
st.divider()

# ── Top Metrics ───────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Jobs", len(df))
col2.metric("Cities", df["job_city"].nunique())
col3.metric("Companies", df["employer_name"].nunique())
col4.metric("Remote Jobs", int(df["job_is_remote"].sum()))

st.divider()

# ── Row 1: Cities + Companies ─────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏙️ Top Cities Hiring")
    city_data = df["job_city"].value_counts().head(10).reset_index()
    city_data.columns = ["City", "Jobs"]
    fig = px.bar(city_data, x="Jobs", y="City",
                 orientation="h", color="Jobs",
                 color_continuous_scale="Blues")
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🏢 Top Hiring Companies")
    company_data = df["employer_name"].value_counts().head(10).reset_index()
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
    for skills in df["skills"].dropna():
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
    remote_df = df["job_is_remote"].map({True: "Remote", False: "On-Site"})
    remote_counts = remote_df.value_counts().reset_index()
    remote_counts.columns = ["Type", "Count"]
    fig = px.pie(remote_counts, names="Type", values="Count",
                 color_discrete_sequence=["#636EFA", "#EF553B"])
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ── Row 3: State wise jobs ────────────────────────────
st.subheader("🗺️ Jobs by State")
state_data = df["job_state"].value_counts().reset_index()
state_data.columns = ["State", "Jobs"]
fig = px.bar(state_data, x="State", y="Jobs",
             color="Jobs", color_continuous_scale="Purples")
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ── Row 4: Job Listings Table ─────────────────────────
st.subheader("📋 All Job Listings")

col1, col2 = st.columns(2)
with col1:
    city_filter = st.selectbox(
        "Filter by City",
        ["All"] + sorted(df["job_city"].dropna().unique().tolist())
    )
with col2:
    remote_filter = st.selectbox(
        "Filter by Type",
        ["All", "Remote", "On-Site"]
    )

filtered = df.copy()
if city_filter != "All":
    filtered = filtered[filtered["job_city"] == city_filter]
if remote_filter == "Remote":
    filtered = filtered[filtered["job_is_remote"] == True]
elif remote_filter == "On-Site":
    filtered = filtered[filtered["job_is_remote"] == False]

st.dataframe(
    filtered[["job_title", "employer_name", "job_city",
              "job_state", "job_is_remote", "skills"]],
    use_container_width=True
)
st.caption(f"Showing {len(filtered)} of {len(df)} jobs")

# ── Manual Refresh Button ─────────────────────────────
st.divider()
if st.button("🔄 Force Refresh Data Now"):
    if os.path.exists("last_fetch.txt"):
        os.remove("last_fetch.txt")
    st.rerun()
