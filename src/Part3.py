import pandas as pd
import os

# Fix path to cleaned_data.csv - go up one directory level to access Data folder
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, '..', 'Data', 'cleaned_data.csv')
# Load data
df = pd.read_csv(data_path)
# High earners (more than 300k)
high_earners = df[df["TotalPay"] > 300000].copy()
# Job Title contains police
police_jobs = df[df["JobTitle"].str.contains("POLICE", case=False, na=False)].copy()
# Employees from year 2013
from_2013 = df[df["Year"] == 2013].copy()
# Fire jobs
fire_jobs = df[df["JobTitle"].str.contains("FIRE", case=False, na=False)].copy()
# Low paid employees
low_payed = df[df["TotalPay"] < 5000].copy()
# Print results
print("\nHigh earners:")
print(high_earners.head())
print("\nPolice Jobs:")
print(police_jobs.head())
print("\nEmployees from 2013:")
print(from_2013.head())
# Save to Data folder (not src folder)
output_dir = os.path.join(script_dir, '..', 'Data')
high_earners.to_csv(os.path.join(output_dir, "high_earners.csv"), index=False)
police_jobs.to_csv(os.path.join(output_dir, "police_jobs.csv"), index=False)
from_2013.to_csv(os.path.join(output_dir, "from_2013.csv"), index=False)
fire_jobs.to_csv(os.path.join(output_dir, "fire_jobs.csv"), index=False)
low_payed.to_csv(os.path.join(output_dir, "low_payed.csv"), index=False)

print("\n✓ All files saved successfully to Data folder!")