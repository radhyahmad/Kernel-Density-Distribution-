#%%
from influxdb import InfluxDBClient
import matplotlib.pyplot as plt 
import argparse
import numpy as np 

values_temp  = []
values_hum = []
timeseries_temp = []
timeseries_hum = []

client = InfluxDBClient(host='localhost', port=8086)
print(client.get_list_database())
#%%
client.switch_database('datasoil')
client.get_list_measurements()

result = client.query('select *from soil')
points_temp = result.get_points()

#%%
for point in points_temp:
    #print("Time: %s, Soil Temperature: %i" % (point['time'], point['soil_temperature']))
    #print("Soil Temperature: %i," % (point['soil_temperature']))
    #print(point['soil_temperature'])
    timeseries_temp.append(point['time'])
    values_temp.append(point['soil_temperature'])

plt.plot(timeseries_temp, values_temp, 'green')
plt.ylabel("Soil Temperature")
plt.xlabel("time")
plt.show()

#%%
points_hum = result.get_points()
for point in points_hum:
    #print("Time: %s, Soil Humidity: %i" % (point['time'], point['soil_humidity']))
    #print("Soil Humidity: %i" % (point['soil_humidity']))
    timeseries_hum.append(point['time'])
    values_hum.append(point['soil_humidity'])

plt.plot(timeseries_hum, values_hum, 'red')
plt.ylabel("Soil Humidity")
plt.xlabel("time")
plt.show()
#%%
plt.scatter(values_temp, values_hum)
plt.xlabel('soil humidity')
plt.ylabel('soil temperature')
plt.show()
#%%
from numpy import mean
from numpy import std
from scipy.stats import spearmanr
from scipy.stats import pearsonr
#%%
print('temp: mean=%.3f stdv=%.3f' % (mean(values_temp), std(values_temp)))
print('hum: mean=%.3f stdv=%.3f' % (mean(values_hum), std(values_hum)))

#corr1, _ = pearsonr(values_temp, values_hum)
#corr2, _ = spearmanr(values_temp, values_hum)
#print('Pearsons correlation: %.3f' % corr1)
#print('Spearsmans correlation: %.3f' % corr2)


#plt.plot(values_temp, values_hum)
#plt.ylabel("Soil Humidity")
#plt.xlabel("Soil Temperature")
#plt.show()

# Draw the scatter plot
#lines = plt.xcorr(values_temp, values_hum, maxlags=9, usevlines=True)
#plt.title('Hypothetical Data: Soil Humidity vs Soil Temperature')
#plt.xlabel('Temperature')
#plt.ylabel('Humidity')    
#plt.grid(True)
#plt.axhline(0, color='red', lw=2)
#plt.show()
#%%
from scipy.stats.kde import gaussian_kde
from scipy.stats import norm

my_pdf_temperature = gaussian_kde(values_temp)
my_pdf_humidty = gaussian_kde(values_hum)

figure = plt.subplot(2, 1, 1)
plt.title("Soil Temperature Histogram", fontsize=14)
plt.hist(values_temp, label='Temperature', density=False, color='C1', alpha=0.5, bins=30)
plt.xlabel("Temperature")
plt.ylabel("Frequency")
plt.legend(fontsize=8)

figure = plt.subplot(2, 1, 2)
plt.title("Soil Humidity Histogram", fontsize=14)
plt.hist(values_hum, label='Humidity', density=False, color='C0', alpha=0.5, bins=30)
plt.xlabel("Humidity")
plt.ylabel("Frequency")

plt.legend(fontsize=8)
plt.tight_layout()
plt.show()

#%%
figure = plt.subplot(2, 1, 1)
ax = figure.axes
plt.title("Kernel Density Estimation Temperature", fontsize=14)
x = np.linspace(0,50)
plt.plot(x, my_pdf_temperature(x), label='Temperature', color = 'C1')
plt.xlabel("Temperature")
plt.ylabel("Probability Distribution")
plt.legend(fontsize=8)

figure = plt.subplot(2,1,2)
ax = figure.axes
plt.title("Kernel Density Estimation Humidity", fontsize=14)
y = np.linspace(0,1023)
plt.plot(y, my_pdf_humidty(y), label='Humidity', color = 'C0')
plt.xlabel("Humidity")
plt.ylabel("Probability Distribution")
plt.legend(fontsize=8)

plt.tight_layout()
plt.show()
