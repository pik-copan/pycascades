# Add modules directory to path
import os
import sys

sys.path.append('')
sys.path.append('../modules/gen')
sys.path.append('../modules/core')

# global imports
import numpy as np
import matplotlib
matplotlib.use("pdf")
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(font_scale=1.)
import itertools
import time
import glob
from PyPDF2 import PdfFileMerger


# private imports from sys.path
from evolve import evolve

#private imports for earth system
from earth_sys.timing import timing
from earth_sys.functions_earth_system import global_functions
from earth_sys.earth import earth_system



###MAIN
long_save_name = "results"
duration = 100000.  #actual real simulation years
t_step = 15		    #Time step per integration step

#######################GLOBAL VARIABLES##############################
#drive coupling strength
strength = 0.25
#drive global mean temperature (GMT) above pre-industrial
GMT = 2.0
#####################################################################


########################Declaration of variables from passed values#######################
sys_var = np.array(sys.argv[2:], dtype=float)
print(sys_var)

#Tipping ranges from distribution
limits_gis, limits_thc, limits_wais, limits_amaz = sys_var[0], sys_var[1], sys_var[2], sys_var[3]

#Probability fractions
# TO GIS
pf_wais_to_gis, pf_thc_to_gis = sys_var[4], sys_var[5]
# TO THC
pf_gis_to_thc, pf_wais_to_thc = sys_var[6], sys_var[7]
# TO WAIS
pf_thc_to_wais, pf_gis_to_wais = sys_var[8], sys_var[9]
# TO AMAZ
pf_thc_to_amaz = sys_var[10]



#Time scale
print("Compute calibration timescale")
#function call for absolute timing and time conversion
time_props = timing()
gis_time, thc_time, wais_time, amaz_time = time_props.timescales()
conv_fac_gis = time_props.conversion()


#include uncertain "+-" links:
plus_minus_links = np.array(list(itertools.product([-1.0, 0.0, 1.0], repeat=2)))
#directories for the Monte Carlo simulation
mc_dir = int(sys_var[-1])

################################# MAIN #################################
#Create Earth System
earth_system = earth_system(gis_time, thc_time, wais_time, amaz_time,
                            limits_gis, limits_thc, limits_wais, limits_amaz,
                            pf_wais_to_gis, pf_thc_to_gis, pf_gis_to_thc,
                            pf_wais_to_thc, pf_gis_to_wais, pf_thc_to_wais, pf_thc_to_amaz)

################################# MAIN LOOP #################################
for kk in plus_minus_links:
    print("Wais to Thc:{}".format(kk[0]))
    print("Thc to Amaz:{}".format(kk[1]))
    
    try:
        os.stat("{}/feedbacks".format(long_save_name))
    except:
        os.mkdir("{}/feedbacks".format(long_save_name))

    try:
        os.stat("{}/feedbacks/network_{}_{}".format(long_save_name, kk[0], kk[1]))
    except:
        os.mkdir("{}/feedbacks/network_{}_{}".format(long_save_name, kk[0], kk[1]))

    try:
        os.stat("{}/feedbacks/network_{}_{}/{}".format(long_save_name, kk[0], kk[1], str(mc_dir).zfill(4) ))
    except:
        os.mkdir("{}/feedbacks/network_{}_{}/{}".format(long_save_name, kk[0], kk[1], str(mc_dir).zfill(4) ))
    
    #save starting conditions
    np.savetxt("{}/feedbacks/network_{}_{}/{}/empirical_values.txt".format(long_save_name, kk[0], kk[1], str(mc_dir).zfill(4)), sys_var)


    output = []

    state_before = [-1, -1, -1, -1] #initial state
    #get back the network of the Earth system
    net = earth_system.earth_network(GMT, strength, kk[0], kk[1])

    # initialize state
    initial_state = [-1, -1, -1, -1]
    ev = evolve(net, initial_state)
    # plotter.network(net)

    # Timestep to integration
    timestep = t_step
    sim_length = duration 
    t_end = sim_length/conv_fac_gis
    ev.integrate(timestep, t_end)

    #save and plot the temporal evolution
    fig = plt.figure()
    # in case integration time should look the same for all runs divide t_arr_saving_structure by timer
    plt.plot(ev.get_timeseries()[0]*conv_fac_gis, ev.get_timeseries()[1][:, 0], color="c", label="GIS")
    plt.plot(ev.get_timeseries()[0]*conv_fac_gis, ev.get_timeseries()[1][:, 1], color="b", label="THC")
    plt.plot(ev.get_timeseries()[0]*conv_fac_gis, ev.get_timeseries()[1][:, 2], color="k", label="WAIS")
    plt.plot(ev.get_timeseries()[0]*conv_fac_gis, ev.get_timeseries()[1][:, 3], color="g", label="AMAZ")

    plt.title("coupling strength: {}, GMT: {}".format(np.round(strength, 2), np.round(GMT, 2)))
    plt.xlabel("time [years]")
    plt.ylabel("system feature f(x) [a.u.]")
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig("{}/feedbacks/network_{}_{}/{}/time_d{:.2f}_GMT{:.1f}.pdf".format(long_save_name, kk[0], kk[1], str(mc_dir).zfill(4), np.round(strength, 2), np.round(GMT, 2)))
    #plt.show()
    plt.clf()
    plt.close()



    #saving structure
    output.append([GMT,
                   ev.get_timeseries()[1][-1, 0],
                   ev.get_timeseries()[1][-1, 1],
                   ev.get_timeseries()[1][-1, 2],
                   ev.get_timeseries()[1][-1, 3],
                   net.get_number_tipped(ev.get_timeseries()[1][-1]),
                   [net.get_tip_states(ev.get_timeseries()[1][-1])[0]].count(True),
                   [net.get_tip_states(ev.get_timeseries()[1][-1])[1]].count(True),
                   [net.get_tip_states(ev.get_timeseries()[1][-1])[2]].count(True),
                   [net.get_tip_states(ev.get_timeseries()[1][-1])[3]].count(True)
                   ])



    #necessary for break condition
    if len(output) != 0:
        #saving structure
        data = np.array(output)
        np.savetxt("{}/feedbacks/network_{}_{}/{}/feedbacks_{:.2f}.txt".format(long_save_name, kk[0], kk[1], str(mc_dir).zfill(4), strength), data)
        gmt = data.T[0]
        state_gis = data.T[1]
        state_thc = data.T[2]
        state_wais = data.T[3]
        state_amaz = data.T[4]


# it is necessary to limit the amount of saved files
# --> compose one pdf file for each network setting and remove the other time-files
current_dir = os.getcwd()
os.chdir("{}/feedbacks/network_{}_{}/{}/".format(long_save_name, kk[0], kk[1], str(mc_dir).zfill(4)))
pdfs = np.array(np.sort(glob.glob("time_d*.pdf"), axis=0))
if len(pdfs) != 0.:
    merger = PdfFileMerger()
    for pdf in pdfs:
        merger.append(pdf)
    merger.write("timelines_complete.pdf")
    os.system("rm time_d*.pdf")
os.chdir(current_dir)


print("Finish")