import numpy as np

NUMBER_OF_CELLS = 416


def random_deforestation_scenario(seed):
    generator = np.random.default_rng(seed=seed)
    cells = list(range(NUMBER_OF_CELLS))
    generator.shuffle(cells)
    return cells


def soares_filho_deforestation_scenario(deforestation_values):
    return list(reversed(sorted(
        range(len(deforestation_values)),
        key=lambda i: deforestation_values[i]
    )))


def east_to_west_deforestation_scenario(longitudes, seed):
    indices = np.arange(len(longitudes))
    _, counts = np.unique(longitudes, return_counts=True)
    grouped_indices = np.split(indices, np.cumsum(counts)[:-1])
    reversed_groups = list(grouped_indices)

    generator = np.random.default_rng(seed=seed)
    cells = [generator.permutation(group) for group in reversed_groups]

    return np.concatenate(cells)
