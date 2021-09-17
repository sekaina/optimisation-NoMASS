from re import T
from matplotlib.pyplot import clabel
import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt    
fig = plt.figure()
fig.set_size_inches(15,10)
#for i in range (1,100,10):
with open('./monitoring/pareto_obj_gen50.csv', 'r') as f:
    Pareto_objective_functions_50=np.array(list(csv.reader (f, delimiter=',')))
Pareto_objective_functions_50=Pareto_objective_functions_50.astype('float64')


x = Pareto_objective_functions_50[:, 0]/97.5 #chauffage
y = Pareto_objective_functions_50[:, 2]/97.5 #cout
z = Pareto_objective_functions_50[:, 1] #inconfort
color = np.array([50]*(len(x)))
axe1 = plt.subplot2grid((2,2),(0,0))
axe1.set_ylabel('Cout global actualisé en euros/m2', fontsize=15)
plot1=axe1.scatter(x, y, c=color, alpha=0.5, marker='+')
#plt.colorbar(plot1,ax=axe1,label="Heures d'inconfort (T>Tconf+2°C)")


axe2 = plt.subplot2grid((2,2),(1,0))
axe2.set_ylabel("Heures d'inconfort (T>Tconf+2°C)", fontsize=15)
axe2.set_xlabel("Besoins de chauffage kWh/m2", fontsize=15)
plot2=axe2.scatter(x, z, c=color, alpha=0.5, marker='+')
#plt.colorbar(plot2,ax=axe2,label="Cout global actualisé en euros")

axe3 = plt.subplot2grid((2,2),(1,1))
axe3.set_xlabel("Cout global actualisé en euros/m2", fontsize=15)
plot3 = axe3.scatter(y, z, c=color, alpha=0.5, marker='+')
#plt.colorbar(plot3,ax=axe3,label="Besoins de chauffage kWh/m2")


fig.legend(loc="right")
plt.savefig('Front de Pareto_objectifs.png')
plt.show()

'''
fig = plt.figure()
plt.scatter(x,y,c=z)
plt.xlabel("Besoins de chauffage kWh")
plt.ylabel('Cout global actualisé en euros')
plt.title('Front de Pareto')
plt.colorbar(label="Heures d'inconfort (T>Tconf+2°C)")
plt.savefig('Front de Pareto_objectifs.png')
'''
    

