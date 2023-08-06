from ThermodynamicCycles.Evaporator import Evaporator
from ThermodynamicCycles.Source import Source
from ThermodynamicCycles.Connect import Fluid_connect
import matplotlib.pyplot as plt

SOURCE=Source.Object()
EVAPORATOR=Evaporator.Object()

SOURCE.fluid="R134a"
SOURCE.Ti_degC=12
SOURCE.Pi_bar=1
SOURCE.F_kgs=1
SOURCE.calculate()

Fluid_connect(EVAPORATOR.Inlet,SOURCE.Outlet)
EVAPORATOR.calculate()

plt.plot(EVAPORATOR.Qevap_i)