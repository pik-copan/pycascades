"""net_factory module that provides functions to generate networks.
Some generators have to be supplied with element and coupling pools,
which are supposed to be lists of element and coupling objects from which
a random one is chosen for each node and edge respectively."""

from core.tipping_network import tipping_network
from core.coupling import linear_coupling

from random import choice,uniform,randint,seed
from copy import deepcopy
import networkx as nx
from math import sqrt,exp,ceil
import numpy as np

def from_nxgraph( G, element_pool, coupling_pool, coupling=None, sd=None):

    if not nx.is_directed(G):
        raise ValueError("Only directed graphs supported!")

    couplings = []
    if coupling == 'uniform':
        seed_list=np.random.randint(0,100*G.number_of_edges(),
                                    size=G.number_of_edges())
        for ind in range(G.number_of_edges()):
            seed(seed_list[ind])
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

def complete_graph( number, element_pool, coupling_pool):
    G = nx.complete_graph(number, nx.DiGraph())
    net = from_nxgraph(G, element_pool, coupling_pool)
    return net

def directed_watts_strogatz_graph(n, degree, beta, element_pool, coupling_pool,
                                  sd=None):
    k = ceil(degree/2)*2
    if k > n:
        raise nx.NetworkXError("k>n, choose smaller k or larger n")
    
    #If k == n, the graph is complete not Watts-Strogatz
    if k == n:
        return nx.complete_graph(n)

    G = nx.Graph()
    nodes = list(range(n))  # nodes are labeled 0 to n-1
    # connect each node to k/2 neighbors
    for j in range(1, k // 2 + 1):
        targets = nodes[j:] + nodes[0:j]  # first j nodes are now last in list
        G.add_edges_from(zip(nodes, targets))
    
    G = nx.DiGraph(G)
    
    while (G.number_of_edges()/G.number_of_nodes()) > degree:
        G.remove_edge(*choice(list(G.edges())))

    edges = deepcopy(G.edges())
    
    for edge in edges:
        if uniform(0,1) < beta:
            G.remove_edge(edge[0],edge[1])
            while True:
                edge = (randint(0, G.number_of_nodes()-1), 
                        randint(0, G.number_of_nodes()-1))
                if not G.has_edge(edge[0], edge[1]) and edge[0] != edge[1]:
                    G.add_edge(edge[0], edge[1])
                    break   
    
    net = from_nxgraph(G, element_pool, coupling_pool)
    return net

def directed_barabasi_albert_graph(number, average_degree, element_pool, 
                                   coupling_pool, sd=None):
    G = G=nx.DiGraph()
    G.add_nodes_from([0,1])
    G.add_edges_from([(0,1),(1,0)])

    while G.number_of_nodes() < number:
        ind = G.number_of_nodes()
        G.add_node( ind )
        for node in G.nodes():
            p = G.degree(node) / G.number_of_edges()
            if uniform(0,1) < p:
                G.add_edge( ind, node)
            if uniform(0,1) < p:
                G.add_edge( node, ind)
    
    deg = G.number_of_edges() / G.number_of_nodes()
    while deg < average_degree:
        node1 = randint(0, number-1)
        node2 = randint(0, number-1)
        if node1 == node2:
            continue
        p = (G.degree(node1) + G.degree(node2)) / (2*G.number_of_edges())
        if uniform(0,1) < p:
            G.add_edge(node1, node2)
        deg = G.number_of_edges() / G.number_of_nodes()
        
    while deg > average_degree:
        edge = (randint(0, number-1), randint(0, number-1))
        if G.has_edge(edge[0],edge[1]):
            G.remove_edge(*edge)
            deg = G.number_of_edges() / G.number_of_nodes()

    net = from_nxgraph(G, element_pool, coupling_pool)
    return net

"""Spatial Graph generated with the Waxman model on a two-dimensional plane"""
def spatial_graph(number, beta, characteristic_length, element_pool,
                  coupling_pool, sd=None):
    
    G = nx.complete_graph(number, nx.DiGraph())
    
    for node in G.nodes(data=True):
        node[1]['pos'] = (uniform(0,1), uniform(0,1))
    
    remove = []
    for edge in G.edges():
        dist = sqrt(pow(G.nodes[edge[1]]['pos'][0] - 
                        G.nodes[edge[0]]['pos'][0], 2) +
                    pow(G.nodes[edge[1]]['pos'][1] - 
                        G.nodes[edge[0]]['pos'][1], 2))
    
        probability = 1 - beta*exp(-dist/characteristic_length)
        if uniform(0,1) < probability:
            remove.append(edge)

    for edge in remove:
        G.remove_edge(*edge)

    net = from_nxgraph(G, element_pool, coupling_pool)
    for node in net.nodes(data=True):
        node[1]['pos'] = G.nodes[node[0]]['pos']
    return net

def random_reciprocity_model(number, p, reciprocity, element_pool,
                             coupling_pool, sd=None):
    G = nx.erdos_renyi_graph(number, p/2, directed=False, seed=sd)
    G = nx.DiGraph(G)
    
    if sd:
        seed(2*sd)
    while nx.reciprocity(G) > reciprocity:
        edge = choice(list(G.edges()))
        G.remove_edge(*edge)
        while True:
            edge = (randint(0, G.number_of_nodes()-1), 
                    randint(0, G.number_of_nodes()-1))
            if not G.has_edge(edge[0], edge[1]) and edge[0] != edge[1]:
                G.add_edge(edge[0], edge[1])
                break
    
    net = from_nxgraph(G, element_pool, coupling_pool)
    return net

def random_clustering_model(number, edge_number, clustering, element_pool,
                            coupling_pool, sd=None):
    if sd:
        seed(2*sd)
    
    G = nx.empty_graph(number, create_using=nx.DiGraph())
    
    while G.number_of_edges() < edge_number:
        n1 = randint(0, G.number_of_nodes()-1)
        n2 = randint(0, G.number_of_nodes()-1)
        n3 = randint(0, G.number_of_nodes()-1)
        if not (n1 == n2 or n2 == n3 or n1 == n3):
            G.add_edges_from([(n1,n2),(n2,n1),(n2,n3),(n3,n2),(n3,n1),(n1,n3)])

    if nx.average_clustering(G) < clustering:
        raise ValueError("Clustering too large too achieve!")

    while nx.average_clustering(G) > clustering:
        edge = choice(list(G.edges()))
        G.remove_edge(*edge)
        while True:
            edge = (randint(0, G.number_of_nodes()-1), 
                    randint(0, G.number_of_nodes()-1))
            if not G.has_edge(edge[0], edge[1]) and edge[0] != edge[1]:
                G.add_edge(edge[0], edge[1])
                break
    
    net = from_nxgraph(G, element_pool, coupling_pool)
    return net

def directed_configuration_model(original_network, element_pool,
                                 coupling_pool, sd=None):
    din=list(d for n, d in original_network.in_degree())
    dout=list(d for n, d in original_network.out_degree())
    G=nx.directed_configuration_model(din,dout, seed=sd)
    G = nx.DiGraph(G)
    G.remove_edges_from(nx.selfloop_edges(G))

    net = from_nxgraph(G, element_pool, coupling_pool)
    return net
