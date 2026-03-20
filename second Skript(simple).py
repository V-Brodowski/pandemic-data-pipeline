import pandas as pd
import os
import sqlite3

# Path to the folder where this script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the source CSV file
csv_file = os.path.join(current_dir, "Historical_Pandemic_Epidemic_Dataset.csv")

# Paths to output results
summary_csv = os.path.join(current_dir, "summary_by_pathogen.csv")
db_file = os.path.join(current_dir, "pandemic_data.db")

# 1. Load data
df = pd.read_csv(csv_file)

# 2. Simple data cleaning
df = df.drop_duplicates()

# Remove rows with missing key data
df = df.dropna(subset=["Pathogen_Type", "Estimated_Deaths", "Estimated_Cases"])

# 3. Data validation - convert to numbers and remove errors
df["Estimated_Deaths"] = pd.to_numeric(df["Estimated_Deaths"], errors="coerce")
df["Estimated_Cases"] = pd.to_numeric(df["Estimated_Cases"], errors="coerce")
df["Case_Fatality_Rate_Pct"] = pd.to_numeric(df["Case_Fatality_Rate_Pct"], errors="coerce")

# Remove rows with empty values after conversion
df = df.dropna(subset=["Pathogen_Type", "Estimated_Deaths", "Estimated_Cases"])

# Logical validation - remove implausible data
df = df[df["Estimated_Deaths"] >= 0]
df = df[df["Estimated_Cases"] >= df["Estimated_Deaths"]]
df = df[df["Case_Fatality_Rate_Pct"] <= 100]

# 4. Grouping: calculate summary statistics by pathogen type
summary = df.groupby("Pathogen_Type", as_index=False).agg(
    total_deaths=("Estimated_Deaths", "sum"),
    total_cases=("Estimated_Cases", "sum"),
    avg_case_fatality_rate=("Case_Fatality_Rate_Pct", "mean"),
    events_count=("Event_Name", "count")
)

# 5. Sort for convenience
summary = summary.sort_values(by="total_deaths", ascending=False)

# 6. Add useful column - percentage of deaths from total
summary["death_percentage"] = (
    summary["total_deaths"] / summary["total_deaths"].sum() * 100
).round(2)

# 7. Save the summary CSV
summary.to_csv(summary_csv, index=False)

# 8. Save to SQLite
conn = sqlite3.connect(db_file)

df.to_sql("raw_pandemics", conn, if_exists="replace", index=False)
summary.to_sql("summary_by_pathogen", conn, if_exists="replace", index=False)

conn.close()

# 9. Print results to terminal
print("✅ Data loaded and processed successfully")

print("\nGeneral statistics:")
print(f"Total events: {len(df)}")
print(f"Total deaths: {df['Estimated_Deaths'].sum():,.0f}")
print(f"Total cases: {df['Estimated_Cases'].sum():,.0f}")

print("\nSummary by pathogen type:")
print(summary)

print(f"\n✅ Summary CSV saved to: {summary_csv}")
print(f"✅ SQLite database saved to: {db_file}")