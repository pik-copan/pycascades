"""net_factory module that provides functions to generate networks.
Some generators have to be supplied with element and coupling pools,
which are supposed to be lists of element and coupling objects from which
a random one is chosen for each node and edge respectively."""

from core.tipping_network import tipping_network
from core.coupling import linear_coupling

from random import choice,uniform,randint,seed,shuffle
import networkx as nx
from math import floor,sqrt,exp
import numpy as np


def pair( element1, element2, coupling_1_to_2, coupling_2_to_1=None):
    
    net = tipping_network()
    
    net.add_element( element1)
    net.add_element( element2)
    net.add_coupling( 0, 1, coupling_1_to_2)
    if not coupling_2_to_1 == None:
        net.add_coupling( 1, 0, coupling_2_to_1)

    return net

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

def complete_graph( number, element_pool, coupling_pool):
    G = nx.complete_graph(number, nx.DiGraph())
    net = from_nxgraph(G, element_pool, coupling_pool)
    return net

def directed_watts_strogatz_graph(number, k, rewiring):
    G = nx.watts_strogatz_graph(number, k, rewiring)
    
    G_new = nx.empty_graph(G.nodes(), create_using=nx.DiGraph())
    for edge in G.edges():
        if uniform(0,1) < 0.5:
            G_new.add_edge(edge[0], edge[1])
        else:
            G_new.add_edge(edge[1], edge[0])
    
    return G_new

def directed_watts_strogatz_graph_transitivity(number, k, transitivity, sd=None):
    G = nx.Graph()
    nodes = list(range(number))
    for j in range(1, k // 2 + 1):
        targets = nodes[j:] + nodes[0:j]
        G.add_edges_from(zip(nodes, targets))
    
    if nx.transitivity(G) < transitivity:
        raise ValueError("Transitivity too large to achieve")
        
    G = nx.DiGraph(G)
    
    if sd:
        seed(2*sd)

    while nx.transitivity(G) > transitivity:
        edge = choice(list(G.edges()))
        G.remove_edge(*edge)
        while True:
            edge = (randint(0, G.number_of_nodes()), 
                    randint(0, G.number_of_nodes()))
            if not G.has_edge(edge[0], edge[1]):
                G.add_edge(edge[0], edge[1])
                break
    return G
"""
def small_world( number, degree, p, element_pool, coupling_pool, sd=None):
    G = nx.DiGraph()
    for ind in range(0, number):
        G.add_node(ind)

    seed(sd)
    k = floor(degree/2) + 1
    link_probability = degree / (2*k)
    for ind1 in range(1,k+1):
        for ind2 in range(ind1, number):
            if uniform(0,1) < link_probability:
                G.add_edge( ind2-ind1, ind2)
            if uniform(0,1) < link_probability:
                G.add_edge( ind2, ind2-ind1 )
        for ind2 in range(0,ind1):
            if uniform(0,1) < link_probability:
                G.add_edge( number-ind1+ind2, ind2)
            if uniform(0,1) < link_probability:
                G.add_edge( ind2, number-ind1+ind2 )

    rewire = []
    for edge in G.edges:
        if uniform(0,1) < p:
            rewire.append(edge)

    for edge in rewire:
        new_edge = (edge[0], randint(0, number-1))
        tries = 0
        while new_edge[0] == new_edge[1] or G.has_edge(*new_edge):
            new_edge = (edge[0], randint(0, number-1))
            tries += 1
            if tries == pow(G.number_of_nodes(),2):
                new_edge = edge
                break
        G.remove_edge(*edge)
        G.add_edge(*new_edge)

    net = from_nxgraph(G, element_pool, coupling_pool)
    return net
"""

def barabasi_albert_graph(number, average_degree, element_pool, coupling_pool,
                          sd=None):
    G = G=nx.DiGraph()
    G.add_nodes_from([0,1])
    G.add_edges_from([(0,1),(1,0)])

    while G.number_of_nodes() < number:
        ind = G.number_of_nodes()
        G.add_node( ind )
        for node in G.nodes:
            p = G.degree(node) / G.number_of_edges()
            print(p)
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
        dist = sqrt(pow(G.node[edge[1]]['pos'][0] - 
                        G.node[edge[0]]['pos'][0], 2) +
                    pow(G.node[edge[1]]['pos'][1] - 
                        G.node[edge[0]]['pos'][1], 2))
    
        probability = 1 - beta*exp(-dist/characteristic_length)
        if uniform(0,1) < probability:
            remove.append(edge)

    for edge in remove:
        G.remove_edge(*edge)

    net = from_nxgraph(G, element_pool, coupling_pool)
    for node in net.nodes(data=True):
        node[1]['pos'] = G.node[node[0]]['pos']
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

def directed_configuration_model_reciprocity(original_network, element_pool,
                                             coupling_pool, sd=None):
    r_list=[]
    in_list=[]
    out_list=[]
    for idx, node in enumerate(original_network.nodes()):
        pred = set(original_network.predecessors(node))
        succ = set(original_network.successors(node))
        overlap = pred & succ
        for rcount in range(len(overlap)):
            r_list.append(idx)
        for in_count in range(len(pred) - len(overlap)):
            in_list.append(idx)
        for out_count in range(len(succ) - len(overlap)):
            out_list.append(idx)

    G=nx.empty_graph(original_network.number_of_nodes(),
                     create_using=nx.DiGraph())
    shuffle(r_list)
    shuffle(in_list)
    shuffle(out_list)
    while in_list:
        while True:
            edge = (randint(0, len(out_list)-1), randint(0, len(in_list)-1))
            if not G.has_edge(in_list[edge[1]], out_list[edge[0]]):
                G.add_edge(out_list.pop(edge[0]), in_list.pop(edge[1]))
                break
    while r_list:
        n1 = r_list.pop()
        if not r_list:
            break
        n2 = r_list.pop()
        G.add_edges_from([(n1, n2), (n2, n1)])
        
    G = nx.DiGraph(G)
    G.remove_edges_from(nx.selfloop_edges(G))
    
    net = from_nxgraph(G, element_pool, coupling_pool)
    return net

def directed_configuration_model_transitivity(original_network, element_pool,
                                              coupling_pool, sd=None):
    reciprocity = nx.reciprocity(original_network)
    G = nx.Graph(original_network)
    
    joint_degree = []
    for node in G.nodes():
        neighbors = G.neighbors(node)
        N = G.subgraph(neighbors)
        comp_sizes = [len(c) for c in sorted(nx.connected_components(N), 
                      key=len, reverse=True)]
        triangles = [x for x in comp_sizes if x > 1]
        degree = [x for x in comp_sizes if x == 1]
        joint_degree.append((sum(triangles)-len(triangles), sum(degree)))

    G = nx.random_clustered_graph(joint_degree)
    
    G = nx.Graph(G)
    G.remove_edges_from(nx.selfloop_edges(G))
    
    G_new = nx.empty_graph(original_network.nodes(), create_using=nx.DiGraph())
    for edge in G.edges():
        if uniform(0,1) < 0.5:
            G_new.add_edge(edge[0], edge[1])
            if uniform(0,1) < reciprocity:
                G_new.add_edge(edge[1], edge[0])
        else:
            G_new.add_edge(edge[1], edge[0])
            if uniform(0,1) < reciprocity:
                G_new.add_edge(edge[0], edge[1])
    
    net = from_nxgraph(G_new, element_pool, coupling_pool)
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
            if not G.has_edge(edge[0], edge[1]):
                G.add_edge(edge[0], edge[1])
                break
    
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