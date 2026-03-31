from services.distribution_service import DistributionService, DeterministicDistributionService


def test_distribution_non_negative():
    ds = DistributionService(seed=1)
    for _ in range(1000):
        assert ds.sample_non_negative_normal(0.0, 10.0) >= 0.0


def test_deterministic_distribution_clamp_negative():
    ds = DeterministicDistributionService([-1, 3])
    assert ds.sample_non_negative_normal(7, 5) == 0.0
    assert ds.sample_non_negative_normal(7, 5) == 3.0
