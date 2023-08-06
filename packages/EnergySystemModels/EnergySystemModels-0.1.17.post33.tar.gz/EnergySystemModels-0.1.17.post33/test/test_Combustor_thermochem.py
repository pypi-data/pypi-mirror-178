from ThermodynamicCycles.Combustion import Combustor_thermochem
from ThermodynamicCycles.Source import Source
from ThermodynamicCycles.Connect import Fluid_connect

#create object
Air_COMB=Source.Object() #Combustion air source
COMB=Combustor_thermochem.Object()

#-----------Inlet parameters--------------
#Combustion air
Air_COMB.Pi_bar=1.5
Air_COMB.F_kgs=0.16884 # recalculated if Combustion power is given (Nominal_Power_kW)
Air_COMB.fluid="air"
Air_COMB.Ti_degC=20 #410
#Fuel
COMB.fuel="NG"
#COMB.burca_name="C3H8"
#Choose one of Air Excess parameters : 
#COMB.phi=0.8445320197044336 #<1
#COMB.AIR_EXCESS=0.18408772748483426 #5%
COMB.products_O2_molRatio=0.03*0
#COMB.Nominal_Power_kW=545 # if it is known the air mass flow rate is recalculated.

#calculation
Air_COMB.calculate()
Fluid_connect(COMB.Inlet,Air_COMB.Outlet)
COMB.calculate()

#print results
print(Air_COMB.df)
print(COMB.df)