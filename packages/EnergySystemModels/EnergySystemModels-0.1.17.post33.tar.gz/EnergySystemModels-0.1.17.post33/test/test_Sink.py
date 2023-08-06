from ThermodynamicCycles.Sink import Sink
#from ThermodynamicCycles.Connect import Fluid_connect

#Create Sink object
SINK=Sink.Object()


#Fluid_connect(SINK.Inlet,SOURCE.Outlet) 
SINK.Inlet.fluid="air"
SINK.Inlet.F_kgs=0.334
SINK.Inlet.P=101325
SINK.Inlet.h=420000

#calculate SINK
SINK.calculate()

#Print result

print(SINK.df)

print(SINK.To_degC)