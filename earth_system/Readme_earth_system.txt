To start the Earth system application, the following steps need to be considered:
1) Choose one line from the Latin hypercube distributed initial conditions file (i.e. one line from the file "lhs_preparator/latin_sh_file_save.txt"). This will initiate the computation of the respective run
2) Result files are safed under the directory results/feedbacks and the respective network setup (there are nine possibilities: [--, -0, -+, 0-, 00, 0+, +-, +0, ++])
3) Under evaluations start the file "tipped_elements.py" and afterwards "tipped_elements_plots.py"