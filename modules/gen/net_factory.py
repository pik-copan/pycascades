"""net_factory module that provides functions to generate networks.
Some generators have to be supplied with element and coupling pools,
which are supposed to be lists of element and coupling objects from which
a random one is chosen for each node and edge respectively."""

from core.tipping_network import tipping_network
from core.coupling import linear_coupling

from random import choice,uniform,randint,seed
import networkx as nx
from math import floor


def pair( element1, element2, coupling_1_to_2, coupling_2_to_1=None):
    
    net = tipping_network()
    
    net.add_element( element1)
    net.add_element( element2)
    net.add_coupling( 0, 1, coupling_1_to_2)
    if not coupling_2_to_1 == None:
        net.add_coupling( 1, 0, coupling_2_to_1)

    return net

def from_nxgraph( G, element_pool, coupling_pool, coupling=None):
    
    if not nx.is_directed(G):
        raise ValueError("Only directed graphs supported!")
    
    couplings = []
    if coupling == 'uniform':
        for ind in range(G.number_of_edges()):
            strength = uniform(coupling_pool[0],coupling_pool[1])
            couplings.append( linear_coupling( strength ) )
    else:
        for ind in range(G.number_of_edges()):
            couplings.append( choice(coupling_pool) )
        

    net = tipping_network()
    
    for node in G.nodes():
        net.add_element(choice(element_pool))

    for ind, edge in enumerate(G.edges()):
        net.add_coupling( edge[0], edge[1], couplings[ind] )

    return net

def nx_chain( number, k, unidirectional = False ):
    if k >= number:
        raise ValueError("k must be smaller than the network size!")

    G = nx.DiGraph()
    for ind in range(0, number):
        G.add_node(ind)

    for ind1 in range(1,k+1):
        for ind2 in range(ind1, number):
            G.add_edge( ind2-ind1, ind2)
            if not unidirectional:
                G.add_edge( ind2, ind2-ind1)

    return G

def k_chain( number, k, element_pool, coupling_pool, unidirectional = False):
    G = nx_chain(number, k, unidirectional)
    net = from_nxgraph(G, element_pool, coupling_pool)
    return net

def nx_ring( number, k, unidirectional = False ):
    G = nx_chain( number, k, unidirectional )
                 
    for ind1 in range(1,k+1):
        for ind2 in range(0,ind1):
            G.add_edge( number-ind1+ind2, ind2)
            if not unidirectional:
                G.add_edge( ind2, number-ind1+ind2 )
                
    return G
                
def k_ring( number, k, element_pool, coupling_pool, unidirectional = False):
    G = nx_ring(number, k, unidirectional)
    net = from_nxgraph(G, element_pool, coupling_pool)
    return net

def fully_connected( number, element_pool, coupling_pool):
    net = tipping_network()
    net = k_ring( number, number-1, element_pool, coupling_pool)
    return net
    
def watts_strogatz_graph( number, degree, p, element_pool, coupling_pool, sd=None):
    G = nx.DiGraph()
    for ind in range(0, number):
        G.add_node(ind)

    seed(sd)
    k = floor(degree/2) + 1
    for ind1 in range(1,k+1):
        for ind2 in range(ind1, number):
            if uniform(ind1,ind1+1) <= degree/2 + 1:
                G.add_edge( ind2-ind1, ind2)
            if uniform(ind1,ind1+1) <= degree/2 + 1:
                G.add_edge( ind2, ind2-ind1 )
        for ind2 in range(0,ind1):
            if uniform(ind1,ind1+1) <= degree/2 + 1:
                G.add_edge( number-ind1+ind2, ind2)
            if uniform(ind1,ind1+1) <= degree/2 + 1:
                G.add_edge( ind2, number-ind1+ind2 )

    rewire = []
    for k in range(1,k+1):
        for n in range(number):
            to_id = n+k
            while to_id > number-1:
                to_id -= number
            if uniform(0,1) < p:
                rewire.append((n,to_id))
            to_id = n-k
            while to_id < 0:
                to_id += number
            if uniform(0,1) < p:
                rewire.append((n,to_id))
            
    for edge in rewire:
        new_edge = (edge[0], randint(0, number-1))
        while new_edge[0] == new_edge[1] or G.has_edge(*new_edge):
            new_edge = (edge[0], randint(0, number-1))
        G.remove_edge(*edge)
        G.add_edge(*new_edge)

    net = from_nxgraph(G, element_pool, coupling_pool)
    return net

def barabasi_albert_graph( number, element_pool, coupling_pool, sd=None):
    G = G=nx.DiGraph()
    G.add_nodes_from([0,1])
    G.add_edges_from([(0,1),(1,0)])

    while G.number_of_nodes() < number:
        ind = G.number_of_nodes()
        G.add_node( ind )
        for node in G.nodes:
            p = G.degree(node) / (4*G.number_of_edges())
            if uniform(0,1) < p:
                G.add_edge( ind, node)
            if uniform(0,1) < p:
                G.add_edge( node, ind)
                
    net = from_nxgraph(G, element_pool, coupling_pool)
    return net
    
def shamrock( leave_number, leave_size, element_pool, coupling_pool):
    
    net = tipping_network()
    
    net_size = leave_number * (leave_size - 1) + 1
    
    for ind in range(0, net_size):
        net.add_element(choice(element_pool))

    ind = 1
    for wing in range(0, leave_number):
        net.add_coupling( 0, ind, choice(coupling_pool))
        for k in range(2, leave_size):
            net.add_coupling( ind, ind+1, choice(coupling_pool))
            ind += 1
        
        net.add_coupling( ind, 0, choice(coupling_pool))
        ind += 1

    return net