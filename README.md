# 📊 India Job Market Trend Analyzer

A real-time job market dashboard that fetches live job postings from top Indian companies and provides insights on hiring trends, in-demand skills, and personalized job recommendations.

🔗 **Live Demo:** https://india-job-market-analyzer.streamlit.app

---

## 🚀 Features

- 📡 **Real-Time Data** — Fetches live job postings using JSearch RapidAPI
- 🏙️ **City wise Analysis** — Hiring trends across 10 major Indian cities
- 🏢 **Company wise Analysis** — Jobs from 20 top companies like TCS, Google, Amazon
- 🔥 **Top Skills Dashboard** — Most in-demand skills in 2026
- 🔍 **Skill Gap Analyzer** — Enter your skills and get a market match score
- 🎯 **Job Recommender** — Get personalized job matches based on your skills
- 📚 **Free Learning Resources** — Direct links to learn missing skills
- 🔎 **Smart Filters** — Filter by city, company and job type
- 🔄 **Auto Refresh** — Data updates automatically every 24 hours

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data cleaning and analysis |
| Plotly | Interactive charts |
| Streamlit | Web dashboard |
| JSearch RapidAPI | Live job data source |
| GitHub | Version control |
| Streamlit Cloud | Free deployment |

---

## 📊 Dataset

- **616 unique job postings** fetched from live API
- **20 top companies** — TCS, Infosys, Google, Amazon, Microsoft and more
- **10 major Indian cities** — Bengaluru, Hyderabad, Mumbai, Pune and more
- **50+ job roles** including fresher and experienced positions
- **80+ skills tracked** across AI, Cloud, DevOps, Web and Data domains

---

## 🔍 Skill Gap Analyzer

Enter your skills and instantly see:
- ✅ Skills you already have
- ❌ Skills you are missing
- 📊 Your market readiness score out of 100
- 📚 Free resources to learn missing skills

---

## 🎯 Job Recommender

Enter your skills and get:
- 🟢 High match jobs (70%+)
- 🟡 Medium match jobs (40-70%)
- 🔴 Low match jobs (below 40%)
- Detailed breakdown of required vs your skills

---

## 📁 Project Structure
job-market-analyzer/

├── app.py              # Main Streamlit dashboard

├── fetch_jobs.py       # API data fetching script

├── clean.py            # Data cleaning script

├── analyze.py          # Data analysis script

├── cleaned_jobs.csv    # Processed job data

├── requirements.txt    # Python dependencies

└── README.md           # Project documentation

---

## ⚙️ How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/your-username/job-market-analyzer.git
cd job-market-analyzer
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API key
Open `fetch_jobs.py` and replace:
```python
API_KEY = "your_api_key_here"
```

### 5. Fetch fresh data
```bash
python fetch_jobs.py
python clean.py
```

### 6. Run the dashboard
```bash
streamlit run app.py
```

---

## 📈 Sample Insights

- 🏆 **Bengaluru** leads with most job openings
- 🔥 **Python, Java, SQL** are top demanded skills
- 🤖 **Generative AI and MLOps** are fastest growing skills
- 🏢 **Wipro and Deloitte** are top hiring companies
- 🏠 **96% jobs** are on-site roles

---

## 🙋 Author

Built with ❤️ as a data analytics portfolio project.

---

## ⭐ Support

If you found this useful, please give it a ⭐ on GitHub!