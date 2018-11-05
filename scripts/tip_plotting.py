import gen.net_factory as fac
from core.evolve import evolve
from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import networkx as nx

import core.coupling as cpl

def plot_states_over_time(tipping_network, id, init, bif_param, max_t_step,
                          t_end, simulation_number='test'):
    '''Method plots evolution of tipping elements over time given by the array
    id. The diagrams are saved in output folder.
    id: array with ids of tipping elements that should be plotted
    init: array with initial conditions for all tipping elements
    bif_param: bifurcation parameters for all tipping elements'''
    ev = evolve(tipping_network, init, bif_param)
    sol = solve_ivp(ev.f, [0, t_end], init, max_step=max_t_step)
    y = np.zeros((2, len(sol.t)))
    for i in [0, 1]:
        y[i, :] = sol.y[id[i], :]

    param = np.ones((len(id), len(sol.t)))
    for i in range(len(id)):
        if id[i] in tipping_network.get_hopf_dict().keys():
            param[i, :] = np.cos(
                tipping_network.get_hopf_dict()[id[i]] * sol.t)

    fig, ax = plt.subplots(len(id), 1)
    for subplt in range(len(id)):
        ax[subplt].plot(sol.t, param[subplt, :] * np.array(y[subplt, :]))
        ax[subplt].set_title('state of node ' + str(id[subplt]) + ' (' +
                             tipping_network.get_node_types()[
                                 id[subplt]] + ') over time')
        ax[subplt].set_xlabel('time')
        ax[subplt].set_ylabel('state of node ' + str(id[subplt]))

    fig.tight_layout()
    fig.savefig('output/' + str(simulation_number) + '_state_over_time')


def plot_phase_plane(tipping_network, id, init, bif_param, max_t_step, t_end,
                     simulation_number='test'):
    '''Method plots phase plane of two tipping_elements of a tipping_network
    given by the input array id.
    To do so, the differential equation of an evolve element of the
    tipping_network is solved using solve_ivp from the scipy.integrate library.
    The resulting diagram is plotted and saved in an output folder.'''

    ev = evolve(tipping_network, init, bif_param)
    sol = solve_ivp(ev.f, [0, t_end], init, max_step=max_t_step)
    y = np.zeros((2, len(sol.t)))
    for i in [0, 1]:
        y[i, :] = sol.y[id[i], :]

    # plot of cartesian coordinates of hopf tipping_elements. Hence,
    # transformation from polar to cartesian coordinates, i.e. the projection
    # of the radius onto the axis

    param = np.ones((2, len(sol.t)))

    for i in [0, 1]:
        if id[i] in tipping_network.get_hopf_dict().keys():
            param[i, :] = np.cos(
                tipping_network.get_hopf_dict()[id[i]] * sol.t)

    f = plt.figure()
    plt.plot(y[0, :] * param[0, :], y[1, :] * param[1, :])
    plt.xlabel('node ' + str(id[0]) + ' (' + tipping_network.get_node_types()[
        id[0]] + ')')
    plt.ylabel('node ' + str(id[1]) + ' (' + tipping_network.get_node_types()[
        id[1]] + ')')
    plt.title('phase plane of node ' + str(id[0]) + ' and node ' + str(id[1]))
    f.savefig('output/' + str(simulation_number) + '_phaseplane_solve_ivp')


def plot_phase_plane_integration(tipping_network, id, init, bif_param,
                                 max_t_step, t_end, simulation_number='test'):
    '''Phase plane of two tipping elements whose ids are given in the id array
    is plotted. The evolution of the tipping network is determined by the
    intergrate() method of evolve. The resulting figure is saved in an output
    folder.'''
    ev = evolve(tipping_network, init, bif_param)
    ev.integrate(max_t_step, t_end)

    # plot of cartesian coordinates of hopf tipping_elements. Hence,
    # transformation from polar to cartesian coordinates
    param = np.ones((len(id), len(ev.times)))
    for i in [0, 1]:
        if id[i] in tipping_network.get_hopf_dict().keys():
            param[i, :] = np.cos(
                tipping_network.get_hopf_dict()[id[i]] * np.array(ev.times))

    f = plt.figure()
    values = np.array(ev.states)
    plt.plot(param[0, :] * values[:, id[0]], param[1, :] * values[:, id[1]])
    plt.xlabel('node ' + str(id[0]) + ' (' + tipping_network.get_node_types()[
        id[0]] + ')')
    plt.ylabel('node ' + str(id[1]) + ' (' + tipping_network.get_node_types()[
        id[1]] + ')')
    plt.title('phase plane of node ' + str(id[0]) + ' and node ' + str(id[1]))
    f.savefig(
        'output/' + str(simulation_number) + '_phaseplane_evolve_integrate')


def plot_total_bif_impact(tipping_network, id, init, bif_param,
                          max_t_step, t_end, simulation_number='test'):
    '''The total bifurcation impact on nodes given by id is plotted. The total
    bifurcation impact Phi is the sum of the critical parameter of the element
    and all incoming couplings from other nodes. The resulting diagram is saved
    in an output folder.'''
    ev = evolve(tipping_network, init, bif_param)
    ev.integrate(max_t_step, t_end)
    values = np.array(ev.states)

    number_of_nodes = len(id)
    bif_evolution = np.zeros((len(values[:, 0]), number_of_nodes))

    for node in id:
        for time_step in range(len(ev.times)):
            bif_evolution[time_step][node] = ev.bif_par_arr[node] \
                                             + ev.bif_impact_of_other_nodes(
                ev.times[time_step], ev.states[time_step], node)

    fig, ax = plt.subplots(number_of_nodes, 1)
    for node in id:
        ax[node].plot(ev.times, bif_evolution[:, node])
        ax[node].set_title(
            'total bifurcation impact on node ' + str(id[node]) + ' (' +
            tipping_network.get_node_types()[id[node]] + ')')
        ax[node].set_xlabel('time')
        ax[node].set_ylabel('total bif impact')
    fig.tight_layout()
    fig.savefig('output/' + str(
        simulation_number) + '_total_bifurcation_impact_on_nodes')


def plot3D_phase_space_hopf(tipping_network, id_hopf, id_x, init, bif_param,
                            max_t_step, t_end, simulation_number='test'):
    '''A 3D phase space of two coupled Hopf tipping elemnts given by id_hopf
    and another tipping element given by id_x is plotted. The resulting diagram
    is saved in an output folder.'''
    ev = evolve(tipping_network, init, bif_param)
    sol = solve_ivp(ev.f, [0, t_end], init, max_step=max_t_step)
    param_hopf_x = np.cos(tipping_network.get_hopf_dict()[id_hopf] * sol.t)
    param_hopf_y = np.sin(tipping_network.get_hopf_dict()[id_hopf] * sol.t)
    param_x = 1
    if id_x in tipping_network.get_hopf_dict().keys():
        param_x = np.cos(tipping_network.get_hopf_dict()[id_x] * sol.t)

    y_hopf = sol.y[id_hopf, :]
    y_x = sol.y[id_x, :]
    f = plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot3D(param_hopf_x * y_hopf, param_hopf_y * y_hopf, param_x * y_x)
    ax.set_xlabel('x of Hopf node ' + str(id_hopf) + ' (' +
                  tipping_network.get_node_types()[id_hopf] + ')')
    ax.set_ylabel('y of Hopf node ' + str(id_hopf) + ' (' +
                  tipping_network.get_node_types()[id_hopf] + ')')
    ax.set_zlabel(
        'node ' + str(id_x) + ' (' + tipping_network.get_node_types()[
            id_x] + ')')
    ax.set_title(
        'phase space of Hopf nodes ' + str(id_hopf) + ' and node ' + str(id_x))
    f.savefig('output/' + str(simulation_number) + '_phase_space_hopf')


def plot3D_phase_space(tipping_network, id, init, bif_param, max_t_step, t_end,
                       simulation_number='test'):
    '''A 3D phase space of three tipping elements given by the array id  is
    plotted. The resulting diagram is saved in an output folder.'''
    ev = evolve(tipping_network, init, bif_param)
    sol = solve_ivp(ev.f, [0, t_end], init, max_step=max_t_step)
    x = sol.y[id[0], :]
    y = sol.y[id[1], :]
    z = sol.y[id[2], :]
    param = np.ones(3, len(sol.t))

    # plot of cartesian coordinates of hopf tipping_elements. Hence,
    # transformation from polar to cartesian coordinates

    for i in [0, 1, 2]:
        if i in tipping_network.get_hopf_dict().keys():
            param[i, :] = np.cos(
                tipping_network.get_hopf_dict()[id[i]] * sol.t)

    f = plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot3D(param[0] * x, param[1] * y, param[2] * z)
    ax.set_xlabel(
        'node ' + str(id[0]) + ' (' + tipping_network.get_node_types()[
            id[0]] + ')')
    ax.set_ylabel(
        'node ' + str(id[1]) + ' (' + tipping_network.get_node_types()[
            id[1]] + ')')
    ax.set_zlabel(
        'node ' + str(id[2]) + ' (' + tipping_network.get_node_types()[
            id[2]] + ')')
    ax.set_title(
        'phase space of nodes ' + str(id[0]) + ', ' + str(id[1]) + ', ' + str(
            id[2]))
    f.savefig('output/' + str(simulation_number) + '_phase_space_3D')


def plot_tipping_network(tipping_network, evolve_element):
    '''The state given by the evolve_element of the tipping_network is plotted.
    Tipped tipping elements are red, non-tipped elements are green.'''
    tip_state = evolve_element.get_tip_state()
    color_map = []
    label_dict = {}
    for node in range(len(evolve_element.bif_par_arr)):
        label_dict.update({node: str(node) + ' (' +
                                 tipping_network.get_node_types()[node] + ')'})
        if tip_state[node]:
            color_map.append('red')
        else:
            color_map.append('green')
    plt.figure()
    nx.draw_networkx(tipping_network, node_color=color_map, labels=label_dict,
                     arrows=True, fond_size=10)


def plot_bif_diag(tipping_network, id_to_plot, bif_array, node_id_bif_par,
                  init_array, t_end,max_time_step, simulation_number='test'):
    '''A bifurcation diagram of the tipping element id_to_plot of the
    tipping_network is plotted, more precisely the solution of the differential
    equations of the tipping_network depending on initial conditions given by
    init_array is plotted over a bifurcation parameter. node_id_bif_par gives
    the id of the node whose critical parameter is varied and displayed on the
    x-axis. bif_array should have size of "number of tipping elements of the
    network"*"number of bifurcation parameters to be examined
    (for one tipping element)".
    bif_array[i,:] should be constant for all i!=node_id_bif_par.
    init_array should have size "number of tipping elements"*"number of initial
    conditions.
    A special case is considered for the labeling: A two-component system with
    node 0 being a Hopf and node 1 being a cusp-like tipping element.
    The resulting diagram is saved in an output folder.'''
    nr_init_per_value = len(init_array[0])
    number_of_plots = len(id_to_plot)
    nr_bif_values = len(bif_array[0])

    if number_of_plots == 1:
        f = plt.figure()
        stable_states = np.zeros((nr_init_per_value, nr_bif_values))
        for bif in range(nr_bif_values):
            """iterating over all bifurcation values given in bif_array"""
            ev = evolve(tipping_network, init_array[:, 0], bif_array[:, bif])
            # initial value of evolve is not used
            for values in range(nr_init_per_value):
                sol = solve_ivp(ev.f, [0, t_end], init_array[:, values],
                                max_step=max_time_step)
                stable_states[values, bif] = sol.y[id_to_plot, len(sol.t) - 1]

        for values in range(nr_init_per_value):
            # special case: network of two nodes: node 0 is hopf, node 1 is cusp
            plt.plot(bif_array[node_id_bif_par[0], :],
                     stable_states[values, :],
                     '.', markersize=2,
                     label='hopf = ' + str(
                         init_array[0, values]) + ' cusp = ' + str(
                         init_array[1, values]))
        plt.legend()
        plt.xlabel('bifurcation parameter of node ' + str(node_id_bif_par[0]))
        plt.ylabel('stationary state of node ' + str(id_to_plot[0]))
        f.savefig('output/' + str(simulation_number) + '_bifurcation_diagram')


    else:
        stable_states = np.zeros(
            (number_of_plots, nr_init_per_value, nr_bif_values))
        for bif in range(nr_bif_values):
            """iterating over all bifurcation values given in bif_array"""
            ev = evolve(tipping_network, init_array[:, 0], bif_array[:, bif])
            # initial value of evolve is not used

            for values in range(nr_init_per_value):
                sol = solve_ivp(ev.f, [0, t_end], init_array[:, values],
                                max_step=max_time_step)
                for plot_nr in range(number_of_plots):
                    node_id = id_to_plot[plot_nr]
                    stable_states[plot_nr, values, bif] = sol.y[
                        node_id, len(sol.t) - 1]

        fig, ax = plt.subplots(number_of_plots, 1)
        for plot_nr in range(number_of_plots):
            """iterating over bifurcation diagrams"""
            node_id = id_to_plot[plot_nr]
            for values in range(nr_init_per_value):
                ax[plot_nr].plot(bif_array[plot_nr, :],
                        stable_states[values, :], '.', markersize=2,
                        label='hopf = ' + str(init_array[0, values]) +
                              ' cusp = ' + str(init_array[1, values]))

            ax[plot_nr].set_title(
                'bifurcation diagram of node ' + str(node_id))
            ax[plot_nr].set_xlabel('bifurcation parameter')
            ax[plot_nr].set_ylabel('stationary state')
            ax[plot_nr].legend()
        fig.tight_layout()
        fig.savefig(
            'output/' + str(simulation_number) + '_bifurcation_diagram')


def plot_cpl_bif_diagram(tipping_network, node_from, node_to, cpl_str_array,
                         init_array, bif_array, id_to_plot, t_end,
                         max_time_step, simulation_number='test'):
    '''A bifurcation diagram of node id_to_plot is created. The coupling
    strength from node node_from to node node_to is varied by values given by
    cpl_str_array and displayed on the x-axis. bif_array gives critical
    parameters of network. init_array should have size "number of tipping
    element"*"number of initial conditions. The solution of solve_ivp of the
    respective differential equation is plotted on the y-axis.
    The resulting diagram is saved in an output folder.
    A special type of network is used for labeling the legend: A two-component
    tipping network, node 0 being a Hopf and node 1 being a cusp-like tipping
    element.'''
    nr_init_per_value = len(init_array[0])
    nr_of_cpl_values = len(cpl_str_array)

    stable_states = np.zeros((nr_init_per_value, nr_of_cpl_values))

    for coupling in range(nr_of_cpl_values):
        node_types = tipping_network.get_node_types()
        c = 'Error'
        if node_types[node_from] == 'cusp':
            if node_types[node_to] == 'cusp':
                c = cpl.linear_coupling(cpl_str_array[coupling])
            else:
                c = cpl.cusp_to_hopf(node_from, node_to,
                                     tipping_network.nodes[node_to][
                                         'data'].get_a(),
                                     cpl_str_array[coupling])
        elif node_types[node_from] == 'hopf':
            # node of origin is Hopf
            if node_types[node_to] == 'cusp':
                c = cpl.hopf_x_to_cusp(node_from, node_to,
                                       tipping_network.nodes[node_from][
                                           'data'].get_b(),
                                       cpl_str_array[coupling])
            else:
                c = cpl.hopf_x_to_hopf(node_from, node_to,
                                       tipping_network.nodes[node_to][
                                           'data'].get_a(),
                                       tipping_network.nodes[node_from][
                                           'data'].get_b(),
                                       cpl_str_array[coupling])
        else:
            print('Error in tip_plotting.plot_cpl_bif_diagram()')
        tipping_network.add_edge(node_from, node_to, data=c)
        ev = evolve(tipping_network, init_array[:, 0], bif_array)

        for values in range(nr_init_per_value):
            sol = solve_ivp(ev.f, [0, t_end], init_array[:, values],
                            max_step=max_time_step)
            stable_states[values, coupling] = sol.y[id_to_plot, len(sol.t) - 1]

    f = plt.figure()
    for values in range(nr_init_per_value):
        plt.plot(cpl_str_array, stable_states[values, :], '.', markersize=2,
                 label='hopf = ' + str(
                     init_array[0, values]) + ' cusp = ' + str(
                     init_array[1, values]))
    plt.legend()
    plt.xlabel('coupling strength')
    plt.ylabel('x*')
    plt.title('stationary state of node ' + str(
        id_to_plot) + ' with respect to coupling from node ' + str(
        node_from) + ' to node ' + str(node_to))
    f.savefig('output/' + str(
        simulation_number) + '_bifurcation_coupling_of_node_' + str(
        id_to_plot))

