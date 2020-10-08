import os
import sys
import numpy as np
import matplotlib.pyplot as plt

import seaborn as sns
sns.set(font_scale=2.5)
sns.set_style("white")

import re
import glob




data = np.sort(glob.glob("plots/network*.txt"))
output = []
for i in data:
    file = np.loadtxt(i)
    output.append(file)
output = np.array(output)
mean = 100*np.mean(output, axis=0)
std = 100*np.std(output, axis=0)


print("Plotting")
fig, ax0 = plt.subplots(figsize=(8, 10))

colors = ["gray", "k", "b", "g"]
labels = ["GIS", "WAIS", "AMOC", "AR"]



plt.rcParams['hatch.linewidth'] = 2.
#ax0.set_title("Number of tipping cascades: {:.0f} +- {:.0f}".format(total, total_err))
ax0.bar(np.arange(4), [mean[0], mean[2], mean[1], mean[3]]/(0.01*mean[4]),
    yerr=[std[0], std[2], std[1], std[3]]/(0.01*mean[4]), 
    color='None', align='center', alpha=0.85, ecolor='k', error_kw=dict(ecolor='k', lw=2, capsize=5, capthick=3, alpha=1.0),
    hatch='xx', edgecolor=colors, lw=2) #default vaules: ecolor='k', error_kw=dict(ecolor='k', lw=2, capsize=5, capthick=2)
ax0.set_xticks(np.arange(4))
ax0.set_xticklabels(labels, rotation="vertical")
#ax0.set_xlabel("Tipping elements")
ax0.set_ylabel("Likelihood of tipping [%]")
ax0.set_yticks(np.arange(0, 80, 10))

fig.tight_layout()
#sns.despine() #no background grid
fig.savefig("plots/tipped_elements.png")
fig.savefig("plots/tipped_elements.pdf")
fig.clf()
plt.close()

print("Finish")