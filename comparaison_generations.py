import matplotlib.pyplot as plt 
import numpy as np
import csv
with open('./monitoring/pareto_obj_gen20.csv', 'r') as f:
    Pareto_objective_functions_20=np.array(list(csv.reader (f, delimiter=',')))
Pareto_objective_functions_20=Pareto_objective_functions_20.astype('float64')
with open('./monitoring/pareto_obj_gen99.csv', 'r') as f:
    Pareto_objective_functions_99=np.array(list(csv.reader (f, delimiter=',')))
Pareto_objective_functions_99=Pareto_objective_functions_99.astype('float64')

x_20 = Pareto_objective_functions_20[:, 0]/97.5 #chauffage
y_20 = Pareto_objective_functions_20[:, 2]/97.5 #cout
z_20 = Pareto_objective_functions_20[:, 1] #inconfort

x_99 = Pareto_objective_functions_99[:, 0]/97.5 #chauffage
y_99 = Pareto_objective_functions_99[:, 2]/97.5 #cout
z_99 = Pareto_objective_functions_99[:, 1] #inconfort

fig = plt.figure()
fig.set_size_inches(15,20)
    
axe1 = plt.subplot2grid((2,2),(0,0))
axe1.set_ylabel('Cout global actualisé en euros/m2', fontsize=15)
plot1=axe1.scatter(x_20, y_20, c='b')
axe1.scatter(x_99, y_99, c='c')
#plt.colorbar(plot1,ax=axe1,label="Heures d'inconfort (T>Tconf+2°C)")


axe2 = plt.subplot2grid((2,2),(1,0))
axe2.set_ylabel("Heures d'inconfort (T>Tconf+2°C)", fontsize=15)
axe2.set_xlabel("Besoins de chauffage kWh/m2", fontsize=15)
plot2=axe2.scatter(x_20, z_20, c='b')
axe2.scatter(x_99, z_99, c='c')
#plt.colorbar(plot2,ax=axe2,label="Cout global actualisé en euros")

axe3 = plt.subplot2grid((2,2),(1,1))
axe3.set_xlabel("Cout global actualisé en euros/m2", fontsize=15)
plot3 = axe3.scatter(y_20, z_20, c='b', label='20')
axe3.scatter(y_99, z_99, c='c', label='99')
#plt.colorbar(plot3,ax=axe3,label="Besoins de chauffage kWh/m2")

fig.legend(loc="right")
plt.savefig('comparaison Front de Pareto_objectifs.png')
plt.show()
