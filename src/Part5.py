import pandas as pd
import os

# Fix path to cleaned_data.csv
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, '..', 'Data', 'cleaned_data.csv')

# Load data
df = pd.read_csv(data_path)

# Calculate various aggregations
average_totalPay_per_year = df.groupby("Year")["TotalPay"].mean()
average_totalPay_per_jobTitle = df.groupby("JobTitle")["TotalPay"].mean()
max_totalPay_per_jobTitle = df.groupby("JobTitle")["TotalPay"].max()
pay_by_job_year = df.groupby(["Year", "JobTitle"])["TotalPay"].mean()

stats_per_year = df.groupby("Year").agg({
    "TotalPay": ["mean", "min", "max", "count"]
})
# Print results
print("\n========== Average Total Pay Per Year ==========")
print(average_totalPay_per_year.to_string())
print("\n========== Average Total Pay Per Job Title ==========")
print(average_totalPay_per_jobTitle.to_string())
print("\n========== Max Total Pay Per Job Title ==========")
print(max_totalPay_per_jobTitle.to_string())
print("\n========== Pay by Job and Year ==========")
print(pay_by_job_year.to_string())
print("\n========== Statistics Per Year ==========")
print(stats_per_year.to_string())