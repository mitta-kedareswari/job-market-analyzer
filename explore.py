import pandas as pd

# Load the data
df = pd.read_csv("data/jobs.csv")

print("="*50)
print("BASIC INFO")
print("="*50)
print(f"Total Jobs: {len(df)}")
print(f"Total Columns: {len(df.columns)}")

print("\n")
print("="*50)
print("COLUMN NAMES")
print("="*50)
for col in df.columns:
    print(col)

print("\n")
print("="*50)
print("FIRST JOB DETAILS")
print("="*50)
print(df.iloc[0])

print("\n")
print("="*50)
print("MISSING VALUES")
print("="*50)
print(df.isnull().sum())