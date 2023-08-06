


# =============================================================================
# Chiller Model (Evaporator + Compressor + Desuperheater + Condenser + Expansion_Valve)
# =============================================================================

# #ThermodynamicCycles
import CoolProp.CoolProp as CP
from ThermodynamicCycles.Evaporator import Evaporator
from ThermodynamicCycles.Compressor import Compressor
from ThermodynamicCycles.Desuperheater import Desuperheater
from ThermodynamicCycles.Expansion_Valve import Expansion_Valve
from ThermodynamicCycles.Condenser import Condenser
from ThermodynamicCycles.Connect import Fluid_connect

#Cycle Parameters
fluid="R134a"
HP=6 #bar 
LP=1 #bar  
superheat=2 #°C 
eta_is=0.8     
Tdischarge_target=42.5 #°C compressor outlet temperature
subcooling=2 #°C
 
# # Same for saturated vapor
#Evaporator
EVAP=Evaporator.Object()
EVAP.fluid=fluid
print("EVAP.fluid=",fluid)
EVAP.Inlet.F_kgs=0.1 #Kg/s
EVAP.Inlet.P=1e5*LP
EVAP.surchauff=superheat
EVAP.Inlet.h= CP.PropsSI('H','P',EVAP.Inlet.P,'T',40+273.15,fluid)   #initialisation pour le calcul en boucle
EVAP.calculate()

print("T1="+str(round(EVAP.T1-273.15,1))+" °C")           
print("H1="+str(round(EVAP.H1/1000,1))+" kJ/kg")
print("S1="+str(round(EVAP.S1/1000,1))+" kJ/kg-K")

print("T2="+str(round(EVAP.T2-273.15,1))+" °C")
print("H2="+str(round(EVAP.H2/1000,1))+" kJ/kg-K")        
print("S2="+str(round(EVAP.S2/1000,1))+" kJ/kg-K")

# ######compresseur

COMP=Compressor.Object()
Fluid_connect(COMP.Inlet,EVAP.Outlet)
COMP.HP=1e5*HP
COMP.eta_is=eta_is
COMP.To=Tdischarge_target
COMP.Tdischarge_target=Tdischarge_target
COMP.calculate()



print("S3is="+str(round(COMP.S3is,1))+"J/kg-K")
print("T3is="+str(round(COMP.T3is-273.15,1))+" °C")
print("H3is="+str(round(COMP.H3is/1000,1))+" kJ/kg-K")         

print("H3ref="+str(round(COMP.H3ref/1000,1))+" kJ/kg-K")
print("T3ref="+str(round(COMP.T3ref-273.15,1))+" °C")
print("S3ref="+str(round(COMP.S3ref/1000,1))+" kJ/kg-K")

print("To="+str(round(COMP.To-273.15,1))+" °C")
print("Ho="+str(round(COMP.Ho/1000,1))+" kJ/kg-K")
print("So="+str(round(COMP.So/1000,1))+" kJ/kg-K")


# ##################Desurchauffeur

DESURCH=Desuperheater.Object()
Fluid_connect(DESURCH.Inlet,COMP.Outlet)
# #  print(DESURCH.Inlet.P)
DESURCH.calculate()

print("T4="+str(round(DESURCH.Tsv-273.15,1))+" °C")
print("H4="+str(round(DESURCH.Hsv/1000,1))+" kJ/kg-K")
print("S4="+str(round(DESURCH.Ssv/1000,1))+" kJ/kg-K")

        # ##################condender
COND=Condenser.Object()
Fluid_connect(COND.Inlet, DESURCH.Outlet)
COND.subcooling=subcooling
COND.calculate()

print("T5="+str(round(COND.Tsl-273.15,1))+" °C")
print("H5="+str(round(COND.Hsl/1000,1))+" kJ/kg-K")
print("S5="+str(round(COND.Ssl/1000,1))+" kJ/kg-K")

print("T6="+str(round(COND.To-273.15,1))+" °C")
print("H6="+str(round(COND.Ho/1000,1))+" kJ/kg-K")    
print("S6="+str(round(COND.So/1000,1))+" kJ/kg-K")

# ########détendeur

DET=Expansion_Valve.Object()
Fluid_connect(DET.Inlet,COND.Outlet)
Fluid_connect(DET.Outlet,EVAP.Inlet)


DET.calculate()
Fluid_connect(EVAP.Inlet,DET.Outlet)
EVAP.calculate()

# # print("BP=",DET.Outlet.P,EVAP.Inlet.P)



# H7 = COND.Ho
print("H7="+str(round(DET.Outlet.h/1000,1))+" kJ/kg-K")

# # T7=CP.PropsSI('T','P',1e5*float(self.Spinbox_BP.get()),'H',H7,self.fluid)
print("T7="+str(round(DET.To-273.15,1))+" °C")
print("S7="+str(round(DET.So/1000,1))+" kJ/kg-K")

# #######Bilan thermique##############################"
print("Qcomp="+str(round(COMP.Qcomp/1000,1))+" kW")
# Qevap=-float(self.Spinbox_m.get())*(DET.Outlet.h-EVAP.H1)
print("Qevap="+str(round(EVAP.Qevap/1000,1))+" kW")
EER=EVAP.Qevap/COMP.Qcomp
print("EER="+str(round(EER,1))+" ")

# Qdesurch=float(self.Spinbox_m.get())*(COMP.Ho-DESURCH.Hsv)
print("Qdesurch="+str(round(DESURCH.Qdesurch/1000,1))+" kW")

# Qcond=float(self.Spinbox_m.get())*(DESURCH.Hsv-COND.Hsl)
print("Qcond="+str(round(COND.Qcond/1000,1))+" kW")

QcondTot=COND.Qcond+DESURCH.Qdesurch
print("QcondTot="+str(round(QcondTot/1000,1))+" kW")

COP=QcondTot/COMP.Qcomp
print("COP="+str(round(COP,1))+" ")
print("Qlosses="+str(round(COMP.Qlosses/1000,1))+" kW")

# =============================================================================
# End Chiller Model
# =============================================================================




# =============================================================================
# AHU Model (Fresh air + Heating Coil + humidifier)
# =============================================================================

#module de calcul des prop d'air humide
from AHU import FreshAir
#Heating Coil Component
from AHU import HeatingCoil
#composant Humidifier (vapeur ou adiabatique)
from AHU.Humidification import Humidifier
# connexion entre les composants
from AHU.Connect import Air_connect

##########Création des Objects
AN=FreshAir.Object()
BC=HeatingCoil.Object()
HMD=Humidifier.Object()



    
#Récupération des données entrées par l'utilisateur
        #AN
AN.m_vol=3000 #m3/h
#print("AN.m_vol = ",AN.m_vol)
AN.T=14 #°C
AN.HR_FreshAir=71 # %
    #BC
BC.T_out_target=15 #°C
    #Humidifier
HMD.HA_out_target=8 #g/Kg dry air

    #calculate les propriétés d'air neuf; !important
AN.calculate()

Air_connect(BC.Inlet,AN.Outlet)
BC.calculate()
    

Air_connect(HMD.Inlet,BC.Outlet)
    
HMD.HumidType="vapeur" #par default : Humdificateur adiabatique
HMD.calculate()


#enregistrer les résultats du module d'air neuf

#Absolute Humidity  g/kg_as

print("Fresh Air Absolute Humidity  g/kg_as",round(AN.HA,1))
# print("HA_FreshAir[r-1] = ",HA_FreshAir[r-1])
#Sat Vapor Pressure  " Pa"

print("Fresh Air Sat Vapor Pressure   Pa",round(AN.Pvsat,0))
#Wet-Bulb Temperature  °C

print("Fresh Air Wet-Bulb Temperature  °C",round(AN.T_hum,1))
#Specific Enthalpy  KJ/Kg_as

print("Fresh Air Specific Enthalpy  KJ/Kg_as",round(AN.h,3))

#enregistrer les résultats de la Coil de préchauffage

# Specific Enthalpy KJ/Kg_as
print("Heating Coil Specific Enthalpy KJ/Kg_as",round(BC.h_out,1))
# Thermal Power  kW"
print("Heating Coil Thermal Power  kW",round(BC.Qth,1))
# Relative Humidity %"
print("Heating Coil Relative Humidity %",round(BC.HR_out,1))
    
print("Humidifier Steam mass flow rate Kg/s",round(HMD.m_water,3))  
print("Humidifier Dry air mass flow rate Kg/s",round(HMD.m_as,3)) 

# =============================================================================
# End AHU Model
# =============================================================================

