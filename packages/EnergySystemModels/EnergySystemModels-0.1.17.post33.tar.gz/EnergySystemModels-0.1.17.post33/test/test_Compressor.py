from ThermodynamicCycles.Source import Source
from ThermodynamicCycles.Compressor import Compressor
from ThermodynamicCycles.Sink import Sink
from ThermodynamicCycles.Connect import Fluid_connect

#Create Compressor Object with Source and fluid Sink
SOURCE=Source.Object()
COMP=Compressor.Object()
SINK=Sink.Object()

#Data Input
SOURCE.Ti_degC=20
SOURCE.fluid="air"
SOURCE.Pi_bar=1
SOURCE.F_Sm3h=500 # is not considered if  COMP.Qcomp is not None

COMP.eta_is=0.80
COMP.Tdischarge_target=80 # (discharge temperature in degC, after cooler)
COMP.HP=7.5*100000 # discharge pressure in Pa
COMP.Qcomp=48745.761 # if Energy Power is given (W) the Mass flow rate is recalculated


#Calculate and Connect Objects
SOURCE.calculate()
Fluid_connect(COMP.Inlet,SOURCE.Outlet)
COMP.calculate()
Fluid_connect(SINK.Inlet,COMP.Outlet)
SINK.calculate()

#Data output (print DataFrame)
print(SOURCE.df)
print(COMP.df)
print(SINK.df)

print(COMP.F_Sm3h)