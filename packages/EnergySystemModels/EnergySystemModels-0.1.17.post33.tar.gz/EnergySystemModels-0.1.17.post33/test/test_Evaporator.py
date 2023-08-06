from ThermodynamicCycles.Evaporator import Evaporator
from ThermodynamicCycles.Source import Source
from ThermodynamicCycles.Connect import Fluid_connect
import matplotlib.pyplot as plt
SOURCE=Source.Object()
EVAPORATOR=Evaporator.Object()

SOURCE.fluid="R134a"
SOURCE.Ti_degC=0
SOURCE.Pi_bar=3
SOURCE.F_kgs=1
SOURCE.calculate()

EVAPORATOR.Tw_inlet=25
EVAPORATOR.m_water_flow=100
Fluid_connect(EVAPORATOR.Inlet,SOURCE.Outlet)
EVAPORATOR.calculate()
print(EVAPORATOR.T1-273.15)
print(EVAPORATOR.T2-273.15)

plt.plot(EVAPORATOR.Qevap_i,EVAPORATOR.Tfluid_i)
plt.plot(EVAPORATOR.Qevap_i,EVAPORATOR.Twater_i)

plt.show()