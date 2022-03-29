

import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
from matplotlib.widgets import Slider, Button

cube = xr.open_zarr( "varysigma_simulations.zarr", consolidated = False)
df = pd.read_csv("network_configs.csv")


fig = plt.figure(dpi=200)
ax = fig.add_subplot(projection='3d')
plt.subplots_adjust(bottom=0.35)
strength_init = 0.0
alpha_init = 2.0
seed_init = 0
GMT_init = 0.0
sigma_init = 0.1
tend_init = 10000
traj = cube.sel(config_id = 0, GMT= GMT_init, seed = seed_init, strength = strength_init, alpha = alpha_init, sigma = sigma_init, time = slice(tend_init))
#row = df[(df.config_id == 0) & (df.GMT == GMT_init) & (df.strength == strength_init) & (df.alpha == alpha_init) & (df.sigma == sigma_init)]#.iloc[0 if alpha_init != 2.0 else 1]
l = ax.plot(traj.GIS, traj.THC, traj.WAIS, lw = 0.2)
#t = ax.set_title(f"Sigma = {row['sigma']}")
ax.set_xlabel("GIS")
ax.set_ylabel("THC")
ax.set_zlabel("WAIS")
ax.set_xlim((-2., 2.))
ax.set_ylim((-2., 2.))
ax.set_zlim((-2., 2.))
ax_seed = plt.axes([0.25, 0.25, 0.65, 0.03])
ax_alpha = plt.axes([0.25, 0.2, 0.65, 0.03])
ax_strength = plt.axes([0.25, 0.15, 0.65, 0.03])
ax_GMT = plt.axes([0.25, 0.1, 0.65, 0.03])
ax_tend = plt.axes([0.25, 0.05, 0.65, 0.03])
ax_sigma = plt.axes([0.25, 0.0, 0.65, 0.03])

s_seed = Slider(
    ax_seed, "Seed", cube.seed.values.min(), cube.seed.values.max(),
    valinit=seed_init, valstep=cube.seed.values
    )

s_alpha = Slider(
    ax_alpha, "Alpha", cube.alpha.values.min(), cube.alpha.values.max(),
    valinit=alpha_init, valstep=cube.alpha.values
    )

s_strength = Slider(
    ax_strength, "Strength", cube.strength.values.min(), cube.strength.values.max(),
    valinit=strength_init, valstep=cube.strength.values
    )

s_GMT = Slider(
    ax_GMT, "GMT", cube.GMT.values.min(), cube.GMT.values.max(),
    valinit=GMT_init, valstep=cube.GMT.values
    )


s_tend = Slider(
    ax_tend, "Tend", cube.time.values.min()+10, cube.time.values.max(),
    valinit=tend_init, valstep=cube.time.values
    )

s_sigma = Slider(
    ax_sigma, "Sigma", -2, 1,#cube.sigma.values.min(), cube.sigma.values.max(),
    valinit=-2, valstep=[-2, -1, 0, 1]
    )

def update(val):
    traj = cube.sel(config_id = 0, GMT= s_GMT.val, seed = s_seed.val, strength = s_strength.val, alpha = s_alpha.val, sigma = 10.**s_sigma.val, time = slice(s_tend.val))
    s_sigma.valtext.set_text(10.**s_sigma.val)
    #row = df[(df.config_id == 0) & (df.GMT == s_GMT.val) & (df.strength == s_strength.val) & (df.alpha == s_alpha.val) & (df.sigma == s_sigma.val)]#.iloc[0 if alpha_init != s_alpha.val else 1]
    l[0].set_data_3d((traj.GIS.values,traj.THC.values,traj.WAIS.values))
    #t.set_text(f"Sigma = {row['sigma']}")
    fig.canvas.draw_idle()


s_seed.on_changed(update)
s_alpha.on_changed(update)
s_strength.on_changed(update)
s_GMT.on_changed(update)
s_tend.on_changed(update)
s_sigma.on_changed(update)

plt.show()