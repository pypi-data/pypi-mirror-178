from ThermodynamicCycles import MixedStorage
from ThermodynamicCycles.Source import Source
from ThermodynamicCycles.Sink import Sink
from ThermodynamicCycles.Connect import Fluid_connect


#lecture d'un fichier excel
#pip install pandas
import pandas as pd
import os
data=pd.read_excel( os.path.join(os.path.dirname(__file__), 'HotWaterStorage.xlsx'))
data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit="%d/%m/%y %H:%M:%S")
rows = data.shape[0]
print(rows)
print(data.columns)

#initialiser les table de sortie
df_result=pd.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)
df_source=pd.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)
df_str=pd.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)
df_sink=pd.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)

#CreateTank Object with Source and fluid Sink
SOURCE=Source.Object()
SINK=Sink.Object()
STR=MixedStorage.Object()

#paramètres
STR.V=4
STR.Tinit_degC=40
STR.t=1*3600 #in seconde

for r in range(1, rows):
#Data Input
    SOURCE.Ti_degC=data["TdegC"][r] 
    SOURCE.fluid="water"
    SOURCE.Pi_bar=1
    SOURCE.F_m3h=data["F_m3h"][r] 

    SOURCE.Timestamp=data["Timestamp"][r]
    STR.Timestamp=data["Timestamp"][r]
    SINK.Timestamp=data["Timestamp"][r]

    #calcul du pas de temps
    Timestamp=data["Timestamp"][r] 
    dt=(data["Timestamp"][r]-data["Timestamp"][r-1]).total_seconds()
    #print(dt)
    STR.t=dt

    
    



    SOURCE.calculate()
    Fluid_connect(STR.Inlet,SOURCE.Outlet)
    STR.calculate()
    Fluid_connect(SINK.Inlet,STR.Outlet)
    SINK.calculate()


    df_str=df_str.append(STR.df.T)
    df_source=df_source.append(SOURCE.df.T)
    df_sink=df_sink.append(SINK.df.T)
  
# Add new column to the DataFrame
df_result=df_str.merge(df_sink, on=['Timestamp']).merge(df_source, on=['Timestamp'])
print(df_result)

with pd.ExcelWriter('output_WaterStorage.xlsx') as writer:                #Création d'un fichier de sortie + Ecriture
    df_result.to_excel(writer, sheet_name='Feuille output',index=False)
    data.to_excel(writer, sheet_name='Feuille input',index=False)


####PLOT#####

# Import Library

import matplotlib.pyplot as plt
df_result.index=df_result['Timestamp']

# to set the plot size
plt.figure(figsize=(16, 8), dpi=100)

# Plot
df_result["str_Ti_degC"].plot(marker="o",label='Tentrèe (°C)', color='orange')
df_result["str_T_degC"].plot(marker="o",label='Tsortie (°C)')
df_result["cumul_Qstr_kWh"].plot(marker="o",label='Energie stockée cumulée (kWh)')
df_result["Qstr_kW"].plot(marker="o",label='Puissance de stockage (kW)')



# Labelling 

plt.xlabel("Date")
plt.ylabel("kWh, kW et °C")
plt.legend()
plt.grid()
plt.title("Stockage d'énergie thermique")

# Display

plt.show()