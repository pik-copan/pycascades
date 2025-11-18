import numpy as np

NUMBER_OF_CELLS = 416


def adaptation_sample(limits, seed):
    beta_randomizer = 2.53
    generator = np.random.default_rng(seed=seed)
    beta_sample = (
        (limits[1] - limits[0])
        * generator.beta(beta_randomizer, beta_randomizer, NUMBER_OF_CELLS)
        + limits[0]
    )
    return beta_sample


def sensitivity_sample(mean_and_std, seed):
    generator = np.random.default_rng(seed=seed)
    cell_sample = generator.normal(loc=mean_and_std[0], scale=mean_and_std[1])
    flow_sample = generator.normal(loc=mean_and_std[2], scale=mean_and_std[3])
    return cell_sample, flow_sample
