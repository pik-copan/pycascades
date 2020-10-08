from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(font_scale=1.25)
from pyDOE import * #function name >>> lhs


#Tipping limits, see Schellnhuber, et al., 2016:
limits_gis = [0.8, 3.2]
limits_thc = [3.5, 6.0]
limits_wais = [0.8, 5.5]
limits_amaz = [3.5, 4.5]

###################################################
#TO GIS
pf_wais_to_gis = [0.1, 0.2]
pf_thc_to_gis = [0.1, 1.]
# TO THC
pf_gis_to_thc = [0.1, 1.]
pf_wais_to_thc = [0.1, 0.3] 
# TO WAIS
pf_thc_to_wais = [0.1, 0.15]
pf_gis_to_wais = [0.1, 1.0]
#TO AMAZ
pf_thc_to_amaz = [0.1, 0.4] 


"""
Latin hypercube sampling
"""
points = np.array(lhs(11, samples=1000)) #give dimensions and sample size, here shown for a Latin hypercube

#rescaling function from latin hypercube
def latin_function(limits, rand):
    resc_rand = limits[0] + (limits[1] - limits[0]) * rand
    return resc_rand

#MAIN
array_limits = []
sh_file = []
for i in range(0, len(points)):
    print(i)

    #TIPPING RANGES
    rand_gis = latin_function(limits_gis, points[i][0])
    rand_thc = latin_function(limits_thc, points[i][1])
    rand_wais = latin_function(limits_wais, points[i][2])
    rand_amaz = latin_function(limits_amaz, points[i][3])

    # PROBABILITY FRACTIONS
    rand_wais_to_gis = latin_function(pf_wais_to_gis, points[i][4])
    rand_thc_to_gis = latin_function(pf_thc_to_gis, points[i][5])
    rand_gis_to_thc = latin_function(pf_gis_to_thc, points[i][6])
    rand_wais_to_thc = latin_function(pf_wais_to_thc, points[i][7])
    rand_thc_to_wais = latin_function(pf_thc_to_wais, points[i][8])
    rand_gis_to_wais = latin_function(pf_gis_to_wais, points[i][9])
    rand_thc_to_amaz = latin_function(pf_thc_to_amaz, points[i][10])


    array_limits.append([rand_gis, rand_thc, rand_wais, rand_amaz,
                         rand_wais_to_gis, rand_thc_to_gis, rand_gis_to_thc,
                         rand_wais_to_thc, rand_thc_to_wais, rand_gis_to_wais, rand_thc_to_amaz])


    sh_file.append(["python ../Main_earth_system.py $SLURM_NTASKS {} {} {} {} {} {} {} {} {} {} {} {}".format(
                         rand_gis, rand_thc, rand_wais, rand_amaz,
                         rand_wais_to_gis, rand_thc_to_gis, rand_gis_to_thc,
                         rand_wais_to_thc, rand_thc_to_wais, rand_gis_to_wais, rand_thc_to_amaz, 
                         str(i).zfill(4) )]) #zfill necessary to construct enough folders for monte carlo runs


array_limits = np.array(array_limits)
np.savetxt("latin_prob.txt", array_limits, delimiter=" ")


#Create .sh file to run on the cluster
sh_file = np.array(sh_file)
np.savetxt("latin_sh_file.txt", sh_file, delimiter=" ", fmt="%s")




#tipping ranges and plots
gis = array_limits.T[0]
thc = array_limits.T[1]
wais = array_limits.T[2]
amaz = array_limits.T[3]


plt.grid(True)
plt.hist(gis, 24, facecolor='c', alpha=0.5, label="GIS")
plt.hist(thc, 25, facecolor='b', alpha=0.5, label="THC")
plt.hist(wais, 47, facecolor='k', alpha=0.5, label="WAIS")
plt.hist(amaz, 10, facecolor='g', alpha=0.5, label="AMAZ")
plt.legend(loc='best')
plt.xlabel("Tipping range [°C]")
plt.ylabel("N [#]")
plt.tight_layout()
plt.savefig("latin_prob_TR.png")
plt.savefig("latin_prob_TR.pdf")
#plt.show()
plt.clf()
plt.close()


#coupling strength
wais_to_gis = array_limits.T[4]
thc_to_gis = array_limits.T[5]
gis_to_thc = array_limits.T[6]
wais_to_thc = array_limits.T[7]
thc_to_wais = array_limits.T[8]
gis_to_wais = array_limits.T[9]
thc_to_amaz_pos = array_limits.T[10]


plt.grid(True)
plt.hist(wais_to_gis, 10, facecolor='c', alpha=0.5, label="wais_to_gis")
plt.hist(thc_to_gis, 100, facecolor='b', alpha=0.5, label="thc_to_gis")
plt.hist(gis_to_thc, 100, facecolor='k', alpha=0.5, label="gis_to_thc")
plt.hist(wais_to_thc, 30, facecolor='r', alpha=0.5, label="wais_to_thc")
plt.hist(thc_to_wais, 5, facecolor='#2D9575', alpha=0.5, label="thc_to_wais")
plt.hist(gis_to_wais, 100, facecolor='#8E58C3', alpha=0.5, label="gis_to_wais")
plt.hist(thc_to_amaz_pos, 40, facecolor='#FF5733', alpha=0.5, label="thc_to_amaz")
plt.legend(loc='best')
plt.xlabel("Probability fraction [a.u.]")
plt.ylabel("N [#]")
plt.tight_layout()
plt.savefig("latin_prob_PF.png")
plt.savefig("latin_prob_PF.pdf")
#plt.show()
plt.clf()
plt.close()

print("Finish")



