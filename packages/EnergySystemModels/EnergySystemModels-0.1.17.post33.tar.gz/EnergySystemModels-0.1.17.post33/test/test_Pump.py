from ThermodynamicCycles.Source import Source
from ThermodynamicCycles.Pump import Pump
from ThermodynamicCycles.Sink import Sink
from ThermodynamicCycles.Connect import Fluid_connect

#Create Compressor Object with Source and fluid Sink
SOURCE=Source.Object()
PUMP=Pump.Object()
SINK=Sink.Object()

#Data Input
SOURCE.Ti_degC=20
SOURCE.fluid="water"
SOURCE.Pi_bar=1
SOURCE.F_m3h=36 # is not considered if  COMP.Qcomp is not None

PUMP.eta=0.7
#PUMP.Tdischarge_target=80 # (discharge temperature in degC, after cooler)
PUMP.Pdischarge_bar=11
#PUMP.Qcomp=48745.761 # if Energy Power is given (W) the Mass flow rate is recalculated
PUMP.X_F=[2,15,30] #points caractéristiques  m3/h
PUMP.Y_hmt=[12,10,5] #points caractéristiques  m
PUMP.Y_eta=[0.3,0.7,0.2] #points de rendement
#Calculate and Connect Objects
SOURCE.calculate()
Fluid_connect(PUMP.Inlet,SOURCE.Outlet)
PUMP.calculate()
Fluid_connect(SINK.Inlet,PUMP.Outlet)
SINK.calculate()

#Data output (print DataFrame)
#print(SOURCE.df)
#print(SINK.df)
#print(PUMP.df)
