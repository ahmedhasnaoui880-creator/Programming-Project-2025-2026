import pandas as pd
df= pd.read_csv("data.csv")

average_totalPay_per_year=df.groupby("Year")["TotalPay"].mean()
average_totalPay_per_jobTitle=df.groupby("JobTitle")["TotalPay"].mean()
max_totalPay_per_jobTitle=df.groupby("JobTitle")["TotalPay"].max()
pay_by_job_year=df.groupby(["Year","JobTitle"])["TotalPay"].mean()
stats_per_year=df.groupby("Year").agg({
    "TotalPay":["mean","min","max","count"]
})
print(average_totalPay_per_year)
print(average_totalPay_per_jobTitle)
print(max_totalPay_per_jobTitle)
print(pay_by_job_year)
print(stats_per_year)

