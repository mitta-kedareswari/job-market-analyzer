import requests
import pandas as pd
import os

API_KEY = "b7ef8fee4bmsh4e9cd5799d84039p1baf55jsn9696df9564e1"  # paste your key

url = "https://jsearch.p.rapidapi.com/search-v2"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}

# We'll fetch multiple job roles to get more data
queries = [
    "data analyst jobs in India",
    "data scientist jobs in India",
    "business analyst jobs in India",
    "python developer jobs in India",
    "machine learning engineer jobs in India"
]

all_jobs = []

for query in queries:
    print(f"Fetching: {query}")
    
    params = {
        "query": query,
        "num_pages": "1",
        "country": "in",
        "language": "en"
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if "data" in data and "jobs" in data["data"]:
        jobs = data["data"]["jobs"]
        all_jobs.extend(jobs)
        print(f"  Got {len(jobs)} jobs")
    else:
        print(f"  No jobs found for this query")

# Save to CSV
os.makedirs("data", exist_ok=True)
df = pd.DataFrame(all_jobs)
df.to_csv("data/jobs.csv", index=False)

print(f"\nDone! Total {len(df)} jobs saved to data/jobs.csv")
print(f"\nColumns available:")
for col in df.columns:
    print(f"  - {col}")