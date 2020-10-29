# pycascades
Python framework for simulating tipping cascades on complex networks

pycascades is developed at the Potsdam Institute for Climate Impact Research, Potsdam, Germany.

## Introduction

**Description paper:** N. Wunderling, J. Krönke, V. Wohlfarth, J. Kohler, J. Heitzig, A. Staal, S. Willner, R. Winkelmann, J.F. Donges, Modelling nonlinear dynamics of interacting tipping elements on complex networks: the PyCascades package, in review (2020).

With pycascades, the dynamics of tipping elements on complex networks can be simulated and with that the preconditions for the emergence of tipping cascades. Two types of dynamical systems with bifurcations are pre-implemented: dynamical systems that possess a Cusp- or a Hopf-bifurcation. Further, arbitrary complex networks of tipping elements can be implemented, and three types of paradigmatic network structures can be used out of the box. These are Erdös-Rényi, Barabási-Albert and Watts-Strogatz networks. Further, stochastic processes can be added to the dynamics of the tipping elements such as Gaussian noise, Lévy our Cauchy processes. Lastly, three explicit examples showcase the capabilities of the pycascades software package: (i) The moisture recycling network of the Amazon rainforest, (ii) interacting climate tipping elements and (iii) an application to the global trade network.

pycascades is developed at the Potsdam Institute for Climate Impact Research (PIK), Research Domains for Earth System Analysis and Complexity Science. Responsible senior scientists at PIK: [Jonathan F. Donges.](https://www.pik-potsdam.de/members/donges) and [Ricarda Winkelmann.](https://www.pik-potsdam.de/members/winkelmann) 

## Literature

pycascades has been used in analyses supporting the following publications:

1) N. Wunderling*, B. Stumpf*, J. Krönke, A. Staal, O. Tuinenburg, R. Winkelmann and J.F. Donges, 2020, [How motifs condition critical thresholds for tipping cascades in complex networks: Linking Micro- to Macro-scales](https://aip.scitation.org/doi/10.1063/1.5142827), Chaos: An Interdisciplinary Journal of Nonlinear Science, 30(4), 043129. *These authors share the first authorship.

2) J. Krönke, N. Wunderling, R. Winkelmann, A. Staal, B. Stumpf, O.A. Tuinenburg, J.F. Donges, 2020, [Dynamics of tipping cascades on complex networks](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.101.042311), Physical Review E, 101(4), p.042311

3) N. Wunderling, J.F. Donges, J. Kurths and R. Winkelmann, [Interacting tipping elements increase risk of climate domino effects under global warming](https://esd.copernicus.org/preprints/esd-2020-18/), Earth System Dynamics Discussions, in review (2020).

4) N. Wunderling, A. Staal, B. Sakschewski, M. Hirota, O.A. Tuinenburg, J.F. Donges, H.M.J. Barbosa*, R. Winkelmann*, [Network dynamics of drought-induced tipping cascades in the Amazon rainforest](https://assets.researchsquare.com/files/rs-71039/v1/Manuscript.pdf), in review (2020), *These authors jointly supervised this study.

5) N. Wunderling, M. Gelbrecht, R. Winkelmann, J. Kurths, J.F. Donges, [Basin stability and limit cycles in a conceptual model for climate tipping cascades](https://arxiv.org/abs/2009.09902), in review (2020).

## Funding

The development of pycascades has been supported by the Leibniz Association (project DominoES), the IRTG 1740/TRP 2015/50-122-0 project funded by DFG and FAPESP, the German National Academic Foundation (Studienstiftung des deutschen Volkes), and the European Research Council (ERC advanced grant project ERA, Earth Resilience in the Anthropocene, ERC-2016-ADG-743080).

## Prerequisites

The following Python 3.x packages are needed to run pycascades:
cartopy, copy, csv, glob, itertools, math, matplotlib, netCDF4, networkx, numpy, os, PyDOE, PyPDF2, re, scipy (odeint), seaborn, sdeint, sys, warnings


## Licence

pycascades is licenced under the BSD 3-Clause License.
See the `LICENSE` file for further information. 
