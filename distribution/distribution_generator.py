from distribution.distribution_enum import DistributionEnum
import numpy as np

class DistributionGenerator:

    @staticmethod
    def get_random(dist: DistributionEnum, distParam, sz=1):
        if dist == DistributionEnum.Exponential:
            res = np.random.exponential(scale=1 / distParam, size=sz)
        elif dist == DistributionEnum.Poisson:
            res = np.random.poisson(lam=distParam, size=sz)
        return res
