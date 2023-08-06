from CoolProp.CoolProp import PropsSI
gamma=PropsSI('ISENTROPIC_EXPANSION_COEFFICIENT','T',273.15+15,'P',101325,'Air')
print(gamma)