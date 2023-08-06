from ThermodynamicCycles.Source import Source

#Create Compressor Object
SOURCE=Source.Object()

#Data Input
SOURCE.Ti_degC=25
SOURCE.Pi_bar=1.01325
SOURCE.fluid="air"
#SOURCE.F_kgs=1.225539
#SOURCE.F_m3s=3725.299011/3600
SOURCE.F_Sm3h=3600
#SOURCE.F_kgh=4411.940477
#SOURCE.F_Sm3s=3600/3600
#SOURCE.F_m3h=3725.299011

#Calculate Object
SOURCE.calculate()

#Data output
print(SOURCE.df)