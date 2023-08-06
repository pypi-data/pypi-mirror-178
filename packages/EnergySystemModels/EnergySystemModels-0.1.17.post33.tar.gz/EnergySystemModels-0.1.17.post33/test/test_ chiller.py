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

###############Create chiller component object ##################
EVAP=Evaporator.Object()
COMP=Compressor.Object()
DESURCH=Desuperheater.Object()
COND=Condenser.Object()
DET=Expansion_Valve.Object()
###############################################################

########################Cycle Inlet Parameters########################
#***************Evaporator parameters*******
fluid="R134a"
EVAP.fluid=fluid
EVAP.Inlet.F_kgs=1 #Kg/s
# T or P evap :
EVAP.LP_bar=2.930154 #bar
#EVAP.Ti_degC=0 #Tevap 
EVAP.surchauff=2 #superheating
EVAP.Inlet.h= CP.PropsSI('H','P',1*1e5,'T',40+273.15,fluid)   #initialisation pour le calcul en boucle
#******************compresseur parameters***********

# give HP or Tcond
#COMP.HP=1e5*10 #Pa
COMP.Tcond_degC=40
COMP.eta_is=0.8 # isentropic efficiency
COMP.Tdischarge_target=80 #°C compressor outlet temperature, neglected if compressor is not cooled
COMP.Qcomp==100000 #in (W) If this value is given, the mass flow rate is calculated /Write None if not used  #in (W) If this value is given, the mass flow rate is calculated
#*************** Condenser parameters**************
COND.subcooling=2 #°C subcooling


#calculation algorithme
EVAP.calculate() # evaporator initialisation
Fluid_connect(COMP.Inlet,EVAP.Outlet)
COMP.calculate()
Fluid_connect(DESURCH.Inlet,COMP.Outlet)
DESURCH.calculate()
Fluid_connect(COND.Inlet, DESURCH.Outlet)
COND.calculate()
Fluid_connect(DET.Inlet,COND.Outlet)
Fluid_connect(DET.Outlet,EVAP.Inlet)
DET.calculate()
Fluid_connect(EVAP.Inlet,DET.Outlet)
EVAP.calculate() # recalculate evaporator

# Cycle performance
EER=EVAP.Qevap/COMP.Qcomp
print("EER="+str(round(EER,1))+" ")
QcondTot=COND.Qcond+DESURCH.Qdesurch
print("QcondTot="+str(round(QcondTot/1000,1))+" kW")
COP=QcondTot/COMP.Qcomp
print("COP="+str(round(COP,1))+" ")

# ####### Print Results#######################"
print(COMP.df)
print(EVAP.df)
print(DESURCH.df)
print(COND.df)
print(DET.df)

# =============================================================================
# End Chiller Model
# =============================================================================