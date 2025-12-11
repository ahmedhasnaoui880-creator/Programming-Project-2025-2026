import pandas as pd
df= pd.read_csv("data.csv")
#high earners (more than 300k)
high_earners=df[df["TotalPay"]>300000].copy()
#Job Title contains police
police_jobs= df[df["JobTitle"].str.contains("POLICE",case=False,na=False)].copy()
#Employees from year 2013
from_2013= df[df["Year"]==2013].copy()

fire_jobs= df[df["JobTitle"].str.contains("FIRE",case=False,na=False)].copy()

low_payed= df[df["TotalPay"]<5000].copy()



print("\nHigh earners: \n",high_earners.head())
print("\Police Jobs: \n",police_jobs.head())
print("\nEmployees from 2013: \n",from_2013.head())

high_earners.to_csv("high_earners.csv",index=False)
police_jobs.to_csv("police_jobs.csv",index=False)
from_2013.to_csv("from_2013.csv",index=False)
fire_jobs.to_csv("fire_jobs.csv",index=False)
low_payed.to_csv("low_payed.csv",index=False)
