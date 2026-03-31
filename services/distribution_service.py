import random


class DistributionService:
    def __init__(self, seed: int = 42):
        self.random = random.Random(seed)

    def sample_non_negative_normal(self, mean: float, std: float) -> float:
        return max(0.0, self.random.gauss(mean, std))


class DeterministicDistributionService(DistributionService):
    def __init__(self, sequence: list[float]):
        self.sequence = sequence
        self.idx = 0

    def sample_non_negative_normal(self, mean: float, std: float) -> float:
        value = self.sequence[self.idx % len(self.sequence)]
        self.idx += 1
        return max(0.0, value)
