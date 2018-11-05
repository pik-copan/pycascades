from core.tipping_element import cusp
from core.tipping_element import hopf
from core.coupling import *
from core.tipping_network import tipping_network

from random import uniform,randint

import networkx as nx

"""net_factory module that provides functions to generate 
   user defined networks from parameters
   Warning: Functions could be outdated and might have to be
   updated to make them work!!!"""


def create_one_cusp(a, b, initial_state):
    tc0 = cusp(0, a, b)
    net = tipping_network()
    net.add_node(0, data=tc0)
    return net


def create_cusp_chain(
        number, a, b, initial_state, cpl_strength, opt='uniform'
):
    if opt == 'uniform':
        pass
    else:
        raise ValueError('Unrecognized option ' + opt)

    net = tipping_network()
    for id in range(0, number):
        tc = cusp(id, a, b)
        net.add_node(id, data=tc)

    for id in range(1, number):
        cpl = linear_coupling(net.nodes[id - 1]['data']
                              , net.nodes[id]['data']
                              , cpl_strength)

    net.add_edge(id - 1, id, weight=cpl_strength, data=cpl)

    return net


def create_two_cusps(a, b, initial_state, cpl_strength,
                     negative_coupling=False):
    net = tipping_network()
    for id in range(0, 2):
        tc = cusp(id, a, b)
        net.add_node(id, data=tc)

    if negative_coupling:
        m_cpl_strength = -cpl_strength
    else:
        m_cpl_strength = cpl_strength

    for id in range(1, 2):
        cpl1 = linear_coupling(net.nodes[id - 1]['data']
                               , net.nodes[id]['data']
                               , cpl_strength)
        cpl2 = linear_coupling(net.nodes[id]['data']
                               , net.nodes[id - 1]['data']
                               , m_cpl_strength)

        net.add_edge(id - 1, id, weight=cpl_strength, data=cpl1)
        net.add_edge(id, id - 1, weight=m_cpl_strength, data=cpl2)

    return net


def create_butterfly(wing_number, wing_size, a, b, initial_state,
                     cpl_strength):
    net = tipping_network()
    net_size = wing_number * (wing_size - 1) + 1
    for id in range(0, net_size):
        tc = cusp(id, a, b)
        net.add_node(id, data=tc)

    id = 1
    for no in range(0, wing_number):
        cpl = linear_coupling(cpl_strength)
        net.add_edge(0, id, weight=cpl_strength, data=cpl)
        for k in range(2, wing_size):
            cpl = linear_coupling(cpl_strength)
            net.add_edge(id, id + 1, weight=cpl_strength, data=cpl)
            id += 1
        cpl = linear_coupling(cpl_strength)
        net.add_edge(id, 0, weight=cpl_strength, data=cpl)
        id += 1

    return net


def create_ring(number, a, b, initial_state, cpl_strength):
    net = tipping_network()
    for id in range(0, number):
        tc = cusp(id, a, b)
        net.add_node(id, data=tc)

    for id in range(1, number):
        cpl = linear_coupling(net.nodes[id - 1]['data']
                              , net.nodes[id]['data']
                              , cpl_strength)

        net.add_edge(id - 1, id, weight=cpl_strength, data=cpl)

    cpl = linear_coupling(net.nodes[number - 1]['data']
                          , net.nodes[0]['data']
                          , cpl_strength)

    net.add_edge(number - 1, 0, weight=cpl_strength, data=cpl)

    return net


def create_erdos_renyi( num, link_probability, a, b, cpl_strength_list
                      , negative_probability=0.0, seed=None ):
    net = nx.erdos_renyi_graph(num, link_probability, seed=seed, directed=True)
    net.__class__ = tipping_network

    for id in net.nodes():
        tc = cusp(id, a, b)
        net.node[id]['data'] = tc

    for id in net.edges():
        cpl_strength = cpl_strength_list[randint(0,len(cpl_strength_list)-1)]
        if uniform(0.0,1.0) > negative_probability:
            cpl = linear_coupling(id[0],id[1],cpl_strength)
            net.edges[id]['data'] = cpl
        else:
            cpl = linear_coupling(id[0],id[1],-cpl_strength)
            net.edges[id]['data'] = cpl

    return net


def create_watts_strogatz(
        num, average_degree, rewiring_probability, a, b,
        cpl_strength, tries=100, negative_coupling=False, seed=None
):
    net = nx.connected_watts_strogatz_graph(num, average_degree,
                                            rewiring_probability,
                                            tries=tries, seed=seed)
    net.__class__ = tipping_network

    for id in net.nodes():
        tc = cusp(id, a, b)
        net.node[id]['data'] = tc

    for id in net.edges():
        if negative_coupling:
            if randint(0, 1):
                net.edges[id]['weight'] = cpl_strength
                cpl = linear_coupling(cpl_strength)
                net.edges[id]['data'] = cpl
            else:
                net.edges[id]['weight'] = -cpl_strength
                cpl = linear_coupling(-cpl_strength)
                net.edges[id]['data'] = cpl
        else:
            net.edges[id]['weight'] = cpl_strength
            cpl = linear_coupling(cpl_strength)
            net.edges[id]['data'] = cpl

    return net


def one_hopf(a, b):
    net = tipping_network()
    hopf_elem = hopf(0, a, b)
    net.add_node(0, data=hopf_elem)
    return net


def one_hopf_one_cusp(a_hopf, b_hopf, a_cusp, b_cusp, hopf_id=0, cusp_id=1,
                      strength_hopf_to_cusp=0, strength_cusp_to_hopf=0):
    net = tipping_network()
    hopf1 = hopf(hopf_id, a_hopf, b_hopf)
    cusp1 = cusp(cusp_id, a_cusp, b_cusp)
    net.add_node(hopf_id, data=hopf1)
    net.add_node(cusp_id, data=cusp1)
    if strength_hopf_to_cusp != 0:
        cpl_h_c = hopf_x_to_cusp(hopf_id, cusp_id, b_hopf,
                                 strength_hopf_to_cusp)
        net.add_edge(hopf_id, cusp_id, data=cpl_h_c)
    if strength_cusp_to_hopf != 0:
        cpl_c_h = cusp_to_hopf(cusp_id, hopf_id, a_hopf, strength_cusp_to_hopf)
        net.add_edge(cusp_id, hopf_id, data=cpl_c_h)
    return net


def two_hopf(a_1, b_1, a_2, b_2, cpl_strength_1_to_2=0, cpl_strength_2_to_1=0):
    net = tipping_network()
    hopf1 = hopf(0, a_1, b_1)
    hopf2 = hopf(1, a_2, b_2)
    net.add_node(0, data=hopf1)
    net.add_node(1, data=hopf2)
    if cpl_strength_1_to_2 != 0:
        cpl_1 = hopf_x_to_hopf(0, 1, a_2, b_1, cpl_strength_1_to_2)
        net.add_edge(0, 1, data=cpl_1)
    if cpl_strength_2_to_1 != 0:
        cpl2 = hopf_x_to_hopf(1, 0, a_1, b_2, cpl_strength_2_to_1)
        net.add_edge(1, 0, data=cpl2)
    return net


def two_cusp(a_1, b_1, a_2, b_2, cpl_1_to_2=0, cpl_2_to_1=0):
    net = tipping_network()
    cusp1 = cusp(0, a_1, b_1)
    cusp2 = cusp(1, a_2, b_2)
    net.add_node(0, data=cusp1)
    net.add_node(1, data=cusp2)
    if cpl_1_to_2 != 0:
        cpl_1 = linear_coupling(cpl_1_to_2)
        net.add_edge(0, 1, data=cpl_1)
    if cpl_2_to_1 != 0:
        cpl_2 = linear_coupling(cpl_2_to_1)
        net.add_edge(1, 0, data=cpl_2)
    return net
