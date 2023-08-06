from CoolProp.CoolProp import PropsSI
import CoolProp.CoolProp as CP


print("Density of Wather/Glycol at -12°C, 101325 Pa:", PropsSI("D", "T", -30+273.15, "P", 101325, "INCOMP::MEG-50%"), "kg/m3")

print("Density of AS40 Aspen Temper -40, Potassium acetate/formate  at -12°C, 101325 Pa:", PropsSI("D", "T", -30+273.15, "P", 101325, "INCOMP::AS40"), "kg/m3")

print(PropsSI('H','T',300,'P',101325,'INCOMP::LiBr-23%'))