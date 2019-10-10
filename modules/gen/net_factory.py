"""net_factory module that provides factory classes to generate networks.
Some generators have to be supplied with element and coupling pools,
which are supposed to be lists of element and coupling objects from which
a random one is chosen for each node and each link, respectively."""
from core.tipping_network import tipping_network

from random import choice,uniform,randint
from random import seed as set_seed
from math import sqrt,exp,ceil
from copy import deepcopy

import networkx as nx


class net_factory:
    """Abstract net_factory. Derive concrete network generators from this 
    class"""
    def __init__(self, element_pool, coupling_pool, seed=None):
        self._element_pool = element_pool
        self._coupling_pool = coupling_pool
        self._seed = seed
        if self._seed:
            set_seed(self._seed)
    
    def _from_nxgraph(self):
        if not self._G:
            raise ValueError("Networkx graph has to be generated first!")
        if not nx.is_directed(self._G):
            raise ValueError("Only directed graphs supported!")

        couplings = []
        for ind in range(self._G.number_of_edges()):
            couplings.append(choice(self._coupling_pool))

        self._net = tipping_network()

        for node in self._G.nodes():
            self._net.add_element(choice(self._element_pool))

        for ind, edge in enumerate(self._G.edges()):
            self._net.add_coupling(edge[0], edge[1], couplings[ind])

    def create(self):
        return None

class complete_graph(net_factory):
    def create(self, node_number):
        self._G = nx.complete_graph(node_number, nx.DiGraph())
        self._from_nxgraph()
        return self._net

class erdos_renyi_graph(net_factory):
    def create(self, node_number, link_probability):
        self._G = nx.erdos_renyi_graph(node_number,
                                       link_probability,
                                       directed = True,
                                       seed = self._seed)
        
        self._from_nxgraph()
        return self._net

class directed_watts_strogatz_graph(net_factory):
    def create(self, node_number, degree, beta):
        k = ceil(degree/2)*2
        if k > node_number:
            raise nx.NetworkXError("k>n, choose smaller k or larger n")
    
        #If k == n, the graph is complete not Watts-Strogatz
        if k == node_number:
            return nx.complete_graph(node_number)

        self._G = nx.Graph()
        nodes = list(range(node_number))  # nodes are labeled 0 to n-1
        # connect each node to k/2 neighbors
        for j in range(1, k // 2 + 1):
            # make first j nodes last in list
            targets = nodes[j:] + nodes[0:j]
            self._G.add_edges_from(zip(nodes, targets))
            
        self._G = nx.DiGraph(self._G)
    
        while (self._G.number_of_edges()/self._G.number_of_nodes()) > degree:
            self._G.remove_edge(*choice(list(self._G.edges())))

        edges = deepcopy(self._G.edges())
    
        for edge in edges:
            if uniform(0,1) < beta:
                self._G.remove_edge(edge[0],edge[1])
                while True:
                    edge = (randint(0, self._G.number_of_nodes()-1), 
                            randint(0, self._G.number_of_nodes()-1))
                    if not self._G.has_edge(edge[0], edge[1]) and edge[0] != edge[1]:
                        self._G.add_edge(edge[0], edge[1])
                        break   

        self._from_nxgraph()
        return self._net

class directed_barabasi_albert_graph(net_factory):
    def create(self, node_number, average_degree):
        self._G = nx.DiGraph()
        self._G.add_nodes_from([0,1])
        self._G.add_edges_from([(0,1),(1,0)])

        while self._G.number_of_nodes() < node_number:
            ind = self._G.number_of_nodes()
            self._G.add_node( ind )
            for node in self._G.nodes:
                p = self._G.degree(node) / self._G.number_of_edges()
                if uniform(0,1) < p:
                    self._G.add_edge( ind, node)
                if uniform(0,1) < p:
                    self._G.add_edge( node, ind)
    
        deg = self._G.number_of_edges() / self._G.number_of_nodes()
        while deg < average_degree:
            node1 = randint(0, node_number-1)
            node2 = randint(0, node_number-1)
            if node1 == node2:
                continue
            p = (self._G.degree(node1) + self._G.degree(node2)) / \
                (2*self._G.number_of_edges())
            if uniform(0,1) < p:
                self._G.add_edge(node1, node2)
            deg = self._G.number_of_edges() / self._G.number_of_nodes()
        
        while deg > average_degree:
            edge = (randint(0, node_number-1), randint(0, node_number-1))
            if self._G.has_edge(edge[0],edge[1]):
                self._G.remove_edge(*edge)
                deg = self._G.number_of_edges() / self._G.number_of_nodes()

        self._from_nxgraph()
        return self._net

class waxman_graph(net_factory):
    """Generate spatial graph with the Waxman model 
    on a two-dimensional plane"""
    def create(self, node_number, beta, characteristic_length):
    
        self._G = nx.complete_graph(node_number, nx.DiGraph())
    
        for node in self._G.nodes(data=True):
            node[1]['pos'] = (uniform(0,1), uniform(0,1))
    
        remove = []
        for edge in self._G.edges():
            dist = sqrt(pow(self._G.node[edge[1]]['pos'][0] - 
                            self._G.node[edge[0]]['pos'][0], 2) +
                        pow(self._G.node[edge[1]]['pos'][1] - 
                            self._G.node[edge[0]]['pos'][1], 2))
    
            probability = 1 - beta*exp(-dist/characteristic_length)
            if uniform(0,1) < probability:
                remove.append(edge)

        for edge in remove:
            self._G.remove_edge(*edge)

        self._from_nxgraph()
        for node in self._net.nodes(data=True):
            node[1]['pos'] = self._G.node[node[0]]['pos']
        return self._net

class random_reciprocity_graph(net_factory):
    def create(self, node_number, link_probability, reciprocity):
        self._G = nx.erdos_renyi_graph(node_number,
                                       link_probability/2,
                                       directed=False,
                                       seed=self._seed)
        self._G = nx.DiGraph(self._G)

        while nx.reciprocity(self._G) > reciprocity:
            edge = choice(list(self._G.edges()))
            self._G.remove_edge(*edge)
            while True:
                edge = (randint(0, self._G.number_of_nodes()-1), 
                        randint(0, self._G.number_of_nodes()-1))
                if not self._G.has_edge(edge[0], edge[1]) and edge[0] != edge[1]:
                    self._G.add_edge(edge[0], edge[1])
                    break
    
        self._from_nxgraph()
        return self._net

class random_clustering_graph(net_factory):
    def create(self, node_number, edge_number, clustering):
        self._G = nx.empty_graph(node_number, create_using=nx.DiGraph())
    
        while self._G.number_of_edges() < edge_number:
            n1 = randint(0, self._G.number_of_nodes()-1)
            n2 = randint(0, self._G.number_of_nodes()-1)
            n3 = randint(0, self._G.number_of_nodes()-1)
            if not (n1 == n2 or n2 == n3 or n1 == n3):
                self._G.add_edges_from([(n1,n2),(n2,n1),(n2,n3),
                                        (n3,n2),(n3,n1),(n1,n3)])

        if nx.average_clustering(self._G) < clustering:
            raise ValueError("Clustering too large too achieve!")

        while nx.average_clustering(self._G) > clustering:
            edge = choice(list(self._G.edges()))
            self._G.remove_edge(*edge)
            while True:
                edge = (randint(0, self._G.number_of_nodes()-1), 
                        randint(0, self._G.number_of_nodes()-1))
                if not self._G.has_edge(edge[0], edge[1]) and \
                       edge[0] != edge[1]:
                    self._G.add_edge(edge[0], edge[1])
                    break
    
        self._from_nxgraph()
        return self._net

class directed_configuration_model(net_factory):
    def create(self, original_network):
        din=list(d for n, d in original_network.in_degree())
        dout=list(d for n, d in original_network.out_degree())

        self._G = nx.directed_configuration_model(din, dout, seed=self._seed)
        self._G = nx.DiGraph(self._G)
        self._G.remove_edges_from(nx.selfloop_edges(self._G))

        self._from_nxgraph()
        return self._net
