from CEE import CEE

#fonctionnement : "1*8h" ,"2*8h" ,"3*8h" ,"3*8h_sansArrWE"
#Equipement_type : "pump","fan","air compressor","chiller"
#puissance_nominale : <=1000 kW , Puissance électrique nominale du moteur entraînant le système moto-régulé (en kW)

CEE.euro_MWhcumac=6

# IND_UT_136, MWh_cumac, Euro=CEE.IND_UT_136("3*8h_ArrWE","fan",1000)
# print(IND_UT_136, MWh_cumac, Euro,)

#IND_UT_136, MWh_cumac, Euro =CEE.IND_UT_136("3*8h_ArrWE","chiller",1000)
#print(IND_UT_136, MWh_cumac, Euro)

# print(CEE.IND_UT_135("2*8h",65,15,10))
#print(CEE.IND_UT_134("3*8h_sansArrWE",6,10000))

# print(CEE.IND_UT_103("1*8h", 4, "ECS", 1000))

# CEE.IND_UT_103("2*8h",5,"ECS",50)

# print(CEE.IND_UT_136("3*8h_ArrWE","fan",100))
# print(CEE.IND_UT_136("3*8h_ArrWE","chiller",100))

# print(CEE.IND_UT_135("2*8h",65,15,100))

# print(CEE.IND_UT_103("1*8h", 4, "ECS", 100))
# print(CEE.IND_UT_103("2*8h",5,"ECS",100))

# print(CEE.IND_UT_131("3*8h_sansArrWE",301,'cylindre',1000/3.14,1000))
# print(CEE.IND_UT_131("3*8h_ArrWE",301,'plan',1000))

# print(CEE.IND_UT_130("3*8h_ArrWE",4000))

#print(CEE.TRA_EQ_101("UTIsup9",1000,50))

print(CEE.TRA_EQ_107("Bateau DEK (1 000 t)","Seine",50000))

#print(CEE.TRA_EQ_108("Autre",5343,5343,1232))



