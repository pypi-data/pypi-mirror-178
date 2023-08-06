from heapq import merge
from unicodedata import numeric
from ThermodynamicCycles.Source import Source
from ThermodynamicCycles.Compressor import Compressor
from ThermodynamicCycles.Sink import Sink
from ThermodynamicCycles.Connect import Fluid_connect

#pip install pandas
import pandas as pd
import os
data=pd.read_excel( os.path.join(os.path.dirname(__file__), 'AirCompHeatRecovery.xlsx'))
#data['Timestamp']=data['Timestamp'].dt.strftime("%d/%m/%y %H:%M")
data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit="%d/%m/%y %H:%M:%S")
rows = data.shape[0]
print(rows)
print(data.columns)

#initialiser les table de sortie
df_result=pd.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)
df_source=pd.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)
df_comp=pd.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)
df_sink=pd.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)

#Create Compressor Object with Source and fluid Sink
SOURCE=Source.Object()
COMP=Compressor.Object()
SINK=Sink.Object()

for r in range(0, rows):



    #Data Input
    SOURCE.Ti_degC=data["Taspi(degC)"][r] 
    SOURCE.fluid="air"
    SOURCE.Pi_bar=data["Patm(bar)"][r]  
    SOURCE.Timestamp=data["Timestamp"][r]
    #SOURCE.F_Sm3h=500 # is not considered if  COMP.Qcomp is not None

    COMP.eta_is=0.80
    COMP.Tdischarge_target=data["Trefoul(degC)"][r]  # (discharge temperature in degC, after cooler)
    COMP.HP=data["Prefoul(bar)"][r]*100000 # discharge pressure in Pa
    COMP.Qcomp=data["Jelec(kW)"][r]*1000 # if Energy Power is given (W) the Mass flow rate is recalculated 
    COMP.Timestamp=data["Timestamp"][r]
    SINK.Timestamp=data["Timestamp"][r]

    #Calculate and Connect Objects
    SOURCE.calculate()
    Fluid_connect(COMP.Inlet,SOURCE.Outlet)
    COMP.calculate()
    Fluid_connect(SINK.Inlet,COMP.Outlet)
    SINK.calculate()
   

    df_comp=df_comp.append(COMP.df.T)
    df_source=df_source.append(SOURCE.df.T)
    df_sink=df_sink.append(SINK.df.T)
  
#Data output (print DataFrame)
print(SOURCE.df)
#print(COMP.df)
#print(SINK.df)


# Add new column to the DataFrame


df_result=df_comp.merge(df_sink, on=['Timestamp']).merge(df_source, on=['Timestamp'])



print(df_result)

with pd.ExcelWriter('output_AC_HeatRecovery.xlsx') as writer:                #Création d'un fichier de sortie + Ecriture
    df_result.to_excel(writer, sheet_name='Feuille output',index=False)
    data.to_excel(writer, sheet_name='Feuille input',index=False)

    
print(df_result.columns)
corr=df_result.drop(columns=["Timestamp","comp_fluid","fluid",'src_fluid','fluid_quality']).astype(float).corr()
print("corr",corr)

with pd.ExcelWriter('corr.xlsx') as writer:                #Création d'un fichier de sortie + Ecriture
    corr.to_excel(writer, sheet_name='corr',index=True)

# Import Library

import matplotlib.pyplot as plt
df_result.index=df_result['Timestamp']

# to set the plot size
plt.figure(figsize=(16, 8), dpi=100)

# Plot
df_result["Qlosses(KW)"].plot(label='Qlosses(KW)', color='orange')
df_result["Qcomp(KW)"].plot(label='Qcomp(KW)')



# Labelling 

plt.xlabel("Date")
plt.ylabel("Puissance (kW)")
plt.title("Puissance thermique récupérable")

# Display
plt.legend()
plt.savefig('heat_recovery.png')
plt.show()
