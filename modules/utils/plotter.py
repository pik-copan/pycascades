"""plotter module

Provide functions to generate some useful plots.
"""
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def network(net, spatial=False, edge_labels=False):
    if spatial:
        pos = {}
        for node in net.nodes(data=True):
            pos[node[0]]=node[1]['pos']
    else:
        pos=nx.circular_layout(net)

    nx.draw_networkx(net,pos)
    if edge_labels:
        labels = {}
        for edge in net.edges(data=True):
            labels[(edge[0], edge[1])] = edge[2]['data']._strength
        nx.draw_networkx_edge_labels(net,pos,edge_labels=labels)
    return plt

def network_tip_states(net, x, spatial=False):
    '''The state given of the tipping_network is plotted.
    Tipped tipping elements are red, non-tipped elements are green.'''
    if spatial:
        pos = {}
        for node in net.nodes(data=True):
            pos[node[0]]=node[1]['pos']
    else:
        pos=nx.circular_layout(net)

    tip_state = net.get_tip_states(x)
    color_map = []
    label_dict = {}
    for node in range(net.number_of_nodes()):
        label_dict.update({node: str(node) + ' (' +
                           net.get_node_types()[node] + ')'})
        if tip_state[node]:
            color_map.append('red')
        else:
            color_map.append('green')
    
    nx.draw_networkx(net, pos, node_color=color_map, labels=label_dict,
                     arrows=True, fond_size=10)
    return plt

def series(t, x, legend=False):
    for i in range(x.shape[1]):
        plt.plot(t, x[:,i], label='$x_'+str(i+1)+'$')
    if legend:
        plt.legend(bbox_to_anchor=(0.2, 0.9), loc=1, borderaxespad=0.)
    plt.xlabel('time')
    plt.ylabel('$x$')
    return plt

def phase_flow(net, xrange, yrange):
    if not net.number_of_nodes() == 2:
        raise ValueError("Function only supported for two-element networks!")
    x,y = np.meshgrid(np.linspace(xrange[0],xrange[1],21), 
                      np.linspace(yrange[0],yrange[1],21))
    
    u, v = np.zeros(x.shape), np.zeros(y.shape)
    n_x , n_y = x.shape
    
    for idx in range(n_x):
        for idy in range(n_y):
            x_val = x[idx,idy]
            y_val = y[idx,idy]
            f = net.f([x_val,y_val], 0)
            u[idx,idy] = f[0]
            v[idx,idy] = f[1]
            
    plt.streamplot(x, y, u, v, color='black')
    return plt

def phase_space(net, xrange, yrange):
    if not net.number_of_nodes() == 2:
        raise ValueError("Function only supported for two-element networks!")
    x,y = np.meshgrid(np.linspace(xrange[0],xrange[1],101), 
                      np.linspace(yrange[0],yrange[1],101))
    r = np.zeros(x.shape)
    n_x , n_y = x.shape
    
    for idx in range(n_x):
        for idy in range(n_y):
            x_val = x[idx,idy]
            y_val = y[idx,idy]
            f = net.f([x_val,y_val], 0)
            r[idx,idy] = np.sqrt(pow(f[0],2)+pow(f[1],2))
            
    plt.contourf(x, y, r, 25)
    return plt

def stability(net,xrange,yrange):
    if not net.number_of_nodes() == 2:
        raise ValueError("Function only supported for two-element networks!")
    x,y = np.meshgrid(np.linspace(xrange[0],xrange[1],201), 
                      np.linspace(yrange[0],yrange[1],201))

    stability = np.zeros(x.shape)
    n_x , n_y = x.shape
    
    for idx in range(n_x):
        for idy in range(n_y):
            x_val = x[idx,idy]
            y_val = y[idx,idy]
            val, vec = np.linalg.eig(net.jac([x_val,y_val],0))
            stable = np.less(val,[0,0])
            
            stability[idx,idy] = sum(stable)
    
    colors = [(0.8, 0.1, 0.1), (0.9, 0.9, 0), (0.1, 0.1, 0.8)]
    cmp = LinearSegmentedColormap.from_list('mylist', colors, N=3)        
    plt.contourf(x, y, stability,levels=[-0.5,0.5,1.5,2.5],cmap=cmp)

    plt.colorbar(ticks=[0,1,2])
    return plt
