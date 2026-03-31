from pathlib import Path
import pytest
import simpy

from config.scenario_config import ScenarioConfig
from services.anchor_repository import AnchorRepository
from services.distribution_service import DeterministicDistributionService
from services.runtime_model_builder import RuntimeModelBuilder
from services.statistics_collector import StatisticsCollector


@pytest.fixture
def env():
    return simpy.Environment()


@pytest.fixture
def stats_collector():
    return StatisticsCollector()


@pytest.fixture
def deterministic_distribution():
    return DeterministicDistributionService([7.0, 7.0, 7.0, 7.0, 7.0])


@pytest.fixture
def anchor_json_path() -> str:
    return str(Path("tests/fixtures/anchors_test.json"))


@pytest.fixture
def anchor_repo(anchor_json_path):
    repo = AnchorRepository(anchor_json_path)
    repo.load()
    return repo


@pytest.fixture
def minimal_scenario():
    return ScenarioConfig(
        simulation_time=120.0,
        mu_interarrival_mean=7.0,
        mu_interarrival_std=5.0,
        conveyor_length=10.0,
        conveyor_speed=0.5,
        buffer_capacity=2,
        buffer_to_store_distance=3.0,
        worker_01_speed=1.0,
        store_dispatch_interval=10.0,
    )


@pytest.fixture
def runtime_model(anchor_repo, minimal_scenario, deterministic_distribution):
    builder = RuntimeModelBuilder(anchor_repo)
    return builder.build(minimal_scenario, distribution=deterministic_distribution)
