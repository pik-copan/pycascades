import scipy.integrate as sc_int
import matplotlib.pyplot as plt
import numpy as np

"""test module to get familiar with dynamics of Hopfbifurcation and their 
implementation"""

def hopf(t, z, a_1, a_2, b_1, b_2, bif_par):
    x = z[0]
    y = z[1]
    return [a_1 * y + a_2 * (bif_par - (pow(x, 2) + pow(y, 2))) * x,
            b_1 * x + b_2 * (bif_par - (pow(x, 2) + pow(y, 2))) * y]

def call_hopf(t, z):
    return hopf(t, z, 0.04, 2, -0.04, 2, 1)

def hopf_bif(t, z, bif_par):
    """method returns differential equation of Hopf system given a bifurcation
    parameter bif_par"""
    a_1 = 0.04
    a_2 = 2
    b_1 = -0.04
    b_2 = 2

    x = z[0]
    y = z[1]
    return [a_1 * y + a_2 * (bif_par - (pow(x, 2) + pow(y, 2))) * x,
            b_1 * x + b_2 * (bif_par - (pow(x, 2) + pow(y, 2))) * y]


bif_par_array = []
min_values = []
max_values = []
bif_par_array_unst = []
unstable_fp = []
bif_step = 0.01
tol = 0.1

for bif in np.arange(-1, 2, bif_step):
    sol = sc_int.solve_ivp(lambda t, z: hopf_bif(t, z, bif), (0, 500),
                           [0.01, 0.01])

    sol_t = sol.t[int(len(sol.t) / 3): len(sol.t) - 1]
    sol_y0 = sol.y[0][int(len(sol.t) / 3): len(sol.t) - 1]
    sol_y1 = sol.y[1][int(len(sol.t) / 3): len(sol.t) - 1]
    bif_par_array.append(bif)
    min_values.append(sol_y0.min())
    max_values.append(sol_y0.max())


    if tol < abs(sol_y0.max()-sol_y0.min()):
        # print('in if: abs= ', abs(sol_y0.max()-sol_y0.min()), 'bif= ', bif)
        sol = sc_int.solve_ivp(lambda t, z: hopf_bif(t, z, bif), (0, -500),
                               [0.01, 0.01])
        unstable_fp.append(sol.y[0][len(sol.y[0])-1])
        # print(sol.y[0][len(sol.y[0])-1])
        bif_par_array_unst.append(bif)

f = plt.figure(1)
plt.plot(bif_par_array,min_values, color='red')
plt.plot(bif_par_array,max_values, color='blue')
plt.plot(bif_par_array_unst,unstable_fp, color='green')
plt.xlabel('bifurcation parameter')
plt.ylabel('fixpoint x*')
plt.legend()
f.show()

g = plt.figure(2)
sol_2 = sc_int.solve_ivp(lambda t, z: hopf_bif(t, z, 1.5), (0, -10), [0.5, 0.5])
time_array = np.linspace(0, -50, 1000)
sol_3 = sc_int.odeint(lambda z, t: hopf_bif(t, z, 1.5), [0.5, 0.5], time_array)
plt.plot(time_array, sol_3[:, 0])
plt.xlabel('time')
plt.ylabel('y')
g.show()

h = plt.figure(3)
plt.plot(sol_2.t, sol_2.y[0])
h.show()

print(min(sol_y0))
print(max(sol_y1))

plt.plot(sol_t,sol_y0)
plt.plot(sol_t,sol_y1)

plt.show()




