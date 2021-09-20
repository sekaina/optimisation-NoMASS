import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

zones=["RDCTHERMALZONE","ZCH1","ZCH2","ZCH3","ZSDB"]
variables=["WINDOWSTATE0:Schedule Value [](TimeStep)","BLINDFRACTION:Schedule Value [](TimeStep)", "NUMBEROFOCCUPANTS:Schedule Value [](TimeStep)"]

#df=pd.read_csv("./modelNoMASS/IDM_NoMASS.csv", index_col="Date/Time", parse_dates=True)
#print(df.columns)
#date=pd.to_datetime("2019/ 01/01  00:05:00")
#df["ZCH3BLINDFRACTION:Schedule Value [](TimeStep) "].plot()
#plt.show()
#plt.savefig('ZCH3BLINDFRACTION.png')
#pd.to_datetime(df['Date/Time'])
#print(df['ZCH1WINDOWSTATE0:Schedule Value [](TimeStep)'].head())
#print(df['Date/Time'])
#
'''for zone in zones:
    for variable in variables:
        df[zone+variable].plot()
        plt.xticks(rotation = 70)
        plt.savefig(zone+variable+'.png')#plt.show()
        plt.clf()

with open("./modelNoMASS/IDM_NoMASS_withYear.csv", "w") as file_out:
    with open ("./modelNoMASS/IDM_NoMASS.csv","r") as file_in:
        for line in file_in:
            file_out.write("2021/"+ line)'''



def my_to_datetime(date_str):
    if date_str[8:10] != '24':
        return pd.to_datetime(date_str, format=' %m/%d  %H:%M:%S')
    date_str = date_str[0:8] + '00' + date_str[10:]
    return pd.to_datetime(date_str, format=' %m/%d  %H:%M:%S') + dt.timedelta(days=1)

print(my_to_datetime(' 04/10  24:00:00'))
df=pd.read_csv("./modelNoMASS/IDM_NoMASS.csv",index_col="Date/Time", parse_dates=True, date_parser=my_to_datetime)
print (df.index)
#df['Date/Time'] = df['Date/Time'].apply(my_to_datetime)
#print(df[' 10/10':' 10/14'])
#pd.to_datetime('04/10 23:00:00', format='%m/%d %H:%M:%S')

df["ZCH3BLINDFRACTION:Schedule Value [](TimeStep) "][:"1900/12/31 23:55:00"].plot()
plt.show()
plt.savefig('ZCH3BLINDFRACTION.png')