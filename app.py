import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter

# ── Page Config ──────────────────────────────────────
st.set_page_config(
    page_title="Job Market Analyzer",
    page_icon="📊",
    layout="wide"
)

# ── Load Data ────────────────────────────────────────
df = pd.read_csv("cleaned_jobs.csv")

# ── Title ────────────────────────────────────────────
st.title("📊 India Job Market Trend Analyzer")
st.markdown("**Real-time insights from live job postings**")
st.divider()

# ── Top Metrics ──────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Jobs", len(df))
col2.metric("Cities", df["job_city"].nunique())
col3.metric("Companies", df["employer_name"].nunique())
remote = df["job_is_remote"].sum()
col4.metric("Remote Jobs", int(remote))

st.divider()

# ── Row 1: Cities + Companies ────────────────────────
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

# ── Row 2: Skills + Remote ───────────────────────────
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

# ── Row 3: State wise jobs ───────────────────────────
st.subheader("🗺️ Jobs by State")
state_data = df["job_state"].value_counts().reset_index()
state_data.columns = ["State", "Jobs"]
fig = px.bar(state_data, x="State", y="Jobs",
             color="Jobs", color_continuous_scale="Purples")
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ── Row 4: Job Listings Table ────────────────────────
st.subheader("📋 All Job Listings")

# Filters
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
    filtered[["job_title", "employer_name", "job_city", "job_state", "job_is_remote", "skills"]],
    use_container_width=True
)

st.caption(f"Showing {len(filtered)} of {len(df)} jobs")
