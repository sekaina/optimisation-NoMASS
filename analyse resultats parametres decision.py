import pandas as pd
header_list=["ep_murs_ext","ep_plancher_haut","ep_plancher_bas","type_fenetre"]
df=pd.read_csv("pareto_param_gen99.csv", names=header_list)
print(df.head())
print(df['type_fenetre'].value_counts())