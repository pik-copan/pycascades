"""cplot module

Provides functions/methods to plot stuff.
"""
import matplotlib.pyplot as plt
import networkx as nx

def network(net):
    pos=nx.spring_layout(net)
    nx.draw_networkx(net,pos)
    nx.draw_networkx_edge_labels(net,pos,edge_labels=nx.get_edge_attributes(net,'weight'))
    plt.show()
    
def series(x_array,y_array):
    plt.plot(x_array,y_array)
    plt.show()