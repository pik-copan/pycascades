import numpy as np
from netCDF4 import Dataset
import glob

#plotting imports
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import cartopy.crs as ccrs
import cartopy.feature as cfeature

import seaborn as sns
sns.set(font_scale=2.5)
sns.set_style("whitegrid")


#Coupling flag
coupling = False



#MAIN
if coupling == True:
	name = "with_coupling"
	directory = "../results/"
else:
	name = "no_coupling"
	directory = "../results/no_coupling/"


years = np.arange(2003, 2004, 1)


output = []
for year in years:
    risk_year = np.loadtxt(directory + "unstable_amaz_{}_rcrit1700_field.txt".format(year))
    output.append(risk_year)
output = np.array(output)
#get average and standard deviation
output_mean = np.mean(output, axis=0)
output_std = np.std(output, axis=0)

#save as text files
np.savetxt("risk_map_mean_{}.txt".format(name), output_mean)
np.savetxt("risk_map_std_{}.txt".format(name), output_std)


########PLOTTING STRUCTURE
print("Plotting sequence")
#get lat lon values from 
net_data = Dataset(np.sort(glob.glob("../data/*.nc"))[0])


#latlon values
lat = net_data.variables["lat"][:]
lon = net_data.variables["lon"][:]

tuples = [(lat[idx],lon[idx]) for idx in range(lat.size)]

lat = np.unique(lat)
lon = np.unique(lon)
lat = np.append(lat, lat[-1]+lat[-1]-lat[-2]) #why do we need to append lat[-1]+lat[-1]-lat[-2]???
lon = np.append(lon, lon[-1]+lon[-1]-lon[-2])

vals_mean_no = np.empty((lat.size,lon.size))
vals_mean_no[:,:] = np.nan
vals_std_no = np.empty((lat.size,lon.size))
vals_std_no[:,:] = np.nan

for idx,x in enumerate(lat):
    for idy,y in enumerate(lon):
        if (x,y) in tuples:
            vals_mean_no[idx,idy] = output_mean[tuples.index((x,y))]
            vals_std_no[idx,idy] = output_std[tuples.index((x,y))]


#Plotting Mean
plt.rc('text', usetex=True)
plt.rc('font', family='serif', size=25)
plt.figure(figsize=(15,10))

ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([275, 320, -22, 15], crs=ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE, linewidth=1)
ax.coastlines('50m')

cmap = plt.get_cmap('Reds')
plt.pcolor(lon-(lon[-1]-lon[-2]) / 2, lat-(lat[-1]-lat[-2]) / 2, 100*vals_mean_no, cmap=cmap)

cbar = plt.colorbar(label='Likelihood of tipping [\%]')
plt.clim([0, 100])

plt.savefig('risk_map_{}.png'.format(name), bbox_inches='tight')
plt.savefig('risk_map_{}.pdf'.format(name), bbox_inches='tight')
#plt.show()
plt.clf()
plt.close()


#Plotting Mean
plt.rc('text', usetex=True)
plt.rc('font', family='serif', size=25)
plt.figure(figsize=(15,10))

ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([275, 320, -22, 15], crs=ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE, linewidth=1)
ax.coastlines('50m')

cmap = plt.get_cmap('Reds')
plt.pcolor(lon-(lon[-1]-lon[-2]) / 2, lat-(lat[-1]-lat[-2]) / 2, 100*vals_std_no, cmap=cmap)

cbar = plt.colorbar(label='Likelihood of tipping [\%]')
plt.clim([0, 100])

plt.savefig('risk_map_std_{}.png'.format(name), bbox_inches='tight')
plt.savefig('risk_map_std_{}.pdf'.format(name), bbox_inches='tight')
#plt.show()
plt.clf()
plt.close()




###################FROM HERE ONWARDS: WITH COUPLING!!!#############################
coupling = True


#MAIN
if coupling == True:
	name = "with_coupling"
	directory = "../results/"
else:
	name = "no_coupling"
	directory = "../results/no_coupling/"


years = np.arange(2003, 2004, 1)


output = []
for year in years:
    risk_year = np.loadtxt(directory + "unstable_amaz_{}_rcrit1700_field.txt".format(year))
    output.append(risk_year)
output = np.array(output)
#get average and standard deviation
output_mean = np.mean(output, axis=0)
output_std = np.std(output, axis=0)

#save as text files
np.savetxt("risk_map_mean_{}.txt".format(name), output_mean)
np.savetxt("risk_map_std_{}.txt".format(name), output_std)


########PLOTTING STRUCTURE
print("Plotting sequence")
#get lat lon values from 
net_data = Dataset(np.sort(glob.glob("../data/*.nc"))[0])
#latlon values
lat = net_data.variables["lat"][:]
lon = net_data.variables["lon"][:]

tuples = [(lat[idx],lon[idx]) for idx in range(lat.size)]

lat = np.unique(lat)
lon = np.unique(lon)
lat = np.append(lat, lat[-1]+lat[-1]-lat[-2]) #why do we need to append lat[-1]+lat[-1]-lat[-2]???
lon = np.append(lon, lon[-1]+lon[-1]-lon[-2])

vals_mean_with = np.empty((lat.size,lon.size))
vals_mean_with[:,:] = np.nan
vals_std_with = np.empty((lat.size,lon.size))
vals_std_with[:,:] = np.nan

for idx,x in enumerate(lat):
    for idy,y in enumerate(lon):
        if (x,y) in tuples:
            vals_mean_with[idx,idy] = output_mean[tuples.index((x,y))]
            vals_std_with[idx,idy] = output_std[tuples.index((x,y))]


#Plotting Mean
plt.rc('text', usetex=True)
plt.rc('font', family='serif', size=25)
plt.figure(figsize=(15,10))

ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([275, 320, -22, 15], crs=ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE, linewidth=1)
ax.coastlines('50m')

cmap = plt.get_cmap('Reds')
plt.pcolor(lon-(lon[-1]-lon[-2]) / 2, lat-(lat[-1]-lat[-2]) / 2, 100*vals_mean_with, cmap=cmap)

cbar = plt.colorbar(label='Likelihood of tipping [\%]')
plt.clim([0, 100])

plt.savefig('risk_map_{}.png'.format(name), bbox_inches='tight')
plt.savefig('risk_map_{}.pdf'.format(name), bbox_inches='tight')
#plt.show()
plt.clf()
plt.close()


#Plotting Mean
plt.rc('text', usetex=True)
plt.rc('font', family='serif', size=25)
plt.figure(figsize=(15,10))

ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([275, 320, -22, 15], crs=ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE, linewidth=1)
ax.coastlines('50m')

cmap = plt.get_cmap('Reds')
plt.pcolor(lon-(lon[-1]-lon[-2]) / 2, lat-(lat[-1]-lat[-2]) / 2, 100*vals_std_with, cmap=cmap)

cbar = plt.colorbar(label='Likelihood of tipping [\%]')
plt.clim([0, 100])

plt.savefig('risk_map_std_{}.png'.format(name), bbox_inches='tight')
plt.savefig('risk_map_std_{}.pdf'.format(name), bbox_inches='tight')
#plt.show()
plt.clf()
plt.close()




####################DIFFERENCE BETWEEN NO COUPLING AND WITH COUPLING###############
#Plotting Mean
print("Final Plot")
plt.rc('text', usetex=True)
plt.rc('font', family='serif', size=25)
plt.figure(figsize=(15,10))

ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([275, 320, -22, 15], crs=ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE, linewidth=1)
ax.coastlines('50m')

cmap = plt.get_cmap('Reds')
plt.pcolor(lon-(lon[-1]-lon[-2]) / 2, lat-(lat[-1]-lat[-2]) / 2, 100*(vals_mean_with - vals_mean_no), cmap=cmap)

cbar = plt.colorbar(label='Likelihood of tipping [\%]')
plt.clim([0, 100])

plt.savefig('risk_map_difference.png', bbox_inches='tight')
plt.savefig('risk_map_difference.pdf', bbox_inches='tight')
#plt.show()
plt.clf()
plt.close()


print("Finish")
