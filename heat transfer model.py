import pandas as pd 

data=pd.read_excel(r"C:\Users\hp\OneDrive\Desktop\heat_data.xlsv.xlsx")

print(data.head())
print(data.columns)

#define constants 

import numpy as np 
cp=4187
di=0.0095
do=0.0127
l=1.6
Ai=np.pi*di*l
Ao=np.pi*do*l

#convert flow rate 

data["m_h"]=data["Fh (lpm)"]/60
data["m_c"]=data["Fc (lpm)"]/60
data["Qh"] = data["m_h"] * cp * (data["T1 "] - data["T2"])
data["Qc"] = data["m_c"] * cp * (data["T4"] - data["T3"])
data["Q"]  = (data["Qh"] + data["Qc"]) / 2
data["dT1"] = np.where(
    data["Mode"] == "Parallel",
    data["T1 "] - data["T3"],
    data["T1 "] - data["T4"]
)


data["dT2"] = np.where(
    data["Mode"] == "Parallel",
    data["T2"] - data["T4"],
    data["T2"] - data["T3"]
)


data["LMTD"] = (data["dT1"] - data["dT2"]) / np.log(data["dT1"]/data["dT2"])
data["U"] = data["Q"] / (Ai * data["LMTD"])
print(data[["Mode","U","LMTD"]])


import matplotlib.pyplot as plt

for mode in data["Mode"].unique():
    subset = data[data["Mode"] == mode]
    plt.plot(subset["Fh (lpm)"], subset["U"], marker='o', label=mode)

plt.xlabel("Flow Rate")
plt.ylabel("Overall Heat Transfer Coefficient (U)")
plt.legend()
plt.show()