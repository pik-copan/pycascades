"""cplot module

Provides functions/methods to plot stuff.
"""
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import networkx as nx
import numpy as np

def network(net):
    pos=nx.spring_layout(net)
    nx.draw_networkx(net,pos)
    nx.draw_networkx_edge_labels( net, pos, edge_labels=nx.get_edge_attributes(
                                                            net, 'weight'))
    plt.show()
    
def series(x_array,y_array):
    plt.plot(x_array,y_array)
    plt.show()
    
def phase_flow(evolve,xrange,yrange):
    #plt.style.use('white_background')
    x,y = np.meshgrid(np.linspace(xrange[0],xrange[1],21), 
                      np.linspace(yrange[0],yrange[1],21))
    c = [0,0]
    u, v = np.zeros(x.shape), np.zeros(y.shape)
    n_x , n_y = x.shape
    
    for idx in range(n_x):
        for idy in range(n_y):
            x_val = x[idx,idy]
            y_val = y[idx,idy]
            f = evolve.f(0,[x_val,y_val],c)
            u[idx,idy] = f[0]
            v[idx,idy] = f[1]
            
    plt.streamplot(x, y, u, v, color='black')
    plt.show()
    
def phase_space(evolve,xrange,yrange, bif_par_arr):
    #plt.style.use('white_background')
    x,y = np.meshgrid(np.linspace(xrange[0],xrange[1],101), 
                      np.linspace(yrange[0],yrange[1],101))
    c = bif_par_arr
    r = np.zeros(x.shape)
    n_x , n_y = x.shape
    
    for idx in range(n_x):
        for idy in range(n_y):
            x_val = x[idx,idy]
            y_val = y[idx,idy]
            f = evolve.f(0,[x_val,y_val],c)
            r[idx,idy] = np.sqrt(pow(f[0],2)+pow(f[1],2))
            
    plt.contourf(x, y, r, 25)
    plt.show()
    
def stability(evolve,xrange,yrange):

    x,y = np.meshgrid(np.linspace(xrange[0],xrange[1],201), 
                      np.linspace(yrange[0],yrange[1],201))
    c = [0,0]
    stability = np.zeros(x.shape)
    n_x , n_y = x.shape
    
    for idx in range(n_x):
        for idy in range(n_y):
            x_val = x[idx,idy]
            y_val = y[idx,idy]
            val, vec = np.linalg.eig(evolve.jac(0,[x_val,y_val],c))
            stable = np.less(val,[0,0])
            
            stability[idx,idy] = sum(stable)
    
    print(stability)
    colors = [(0.8, 0.1, 0.1), (0.9, 0.9, 0), (0.1, 0.1, 0.8)]
    cmp = LinearSegmentedColormap.from_list('mylist', colors, N=3)        
    plt.contourf(x, y, stability,levels=[-0.5,0.5,1.5,2.5],cmap=cmp)

    plt.colorbar(ticks=[0,1,2])