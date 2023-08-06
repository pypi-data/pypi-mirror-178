from PinchAnalysis.PinchCalculation import PinchCalculation
import pandas as pd
import matplotlib.pyplot as plt

df=pd.DataFrame({'id': [1, 2, 3, 4],
                   'name': ['stream1', 'stream2', 'stream3', 'stream4'],
                   'Ti': [200, 50, 125, 45],
                 'To': [50, 250, 124, 195],
                 'mCp': [3, 2,300,4],
                 'dTmin2': [5, 5, 10, 10],
                 'integration': [True, True, True, True]
                 })

print(df["To"])

T, plot_GCC, plot_ccf,plot_ccc,utilite_froide,utilite_chaude=PinchCalculation(df)
print("T",T)
print("GCC",plot_GCC[:,0])
print("ccf",plot_ccf[:,0])
print("ccc",plot_ccc[:,0])
print("utilite_froide",utilite_froide)
print("uilite_chaude",utilite_chaude)


# plot the data

fig, (ax1, ax2) = plt.subplots(1, 2)

ax1.plot(plot_ccf[:,0],T, color='tab:blue')
ax1.plot(plot_ccc[:,0],T, color='tab:red')
ax2.plot(plot_GCC[:,0],T, color='tab:orange')

ax1.set(xlabel='kW', ylabel='Temperature (°C)')
ax2.set(xlabel='kW')

ax1.grid(True)
ax2.grid(True)

plt.show()