from dataclasses import dataclass


@dataclass
class ScenarioConfig:
    simulation_time: float = 3600.0
    mu_interarrival_mean: float = 7.0
    mu_interarrival_std: float = 5.0
    conveyor_length: float = 10.0
    conveyor_speed: float = 0.6
    buffer_capacity: int = 10
    buffer_to_store_distance: float = 3.0
    worker_01_speed: float = 0.7
    store_dispatch_interval: float = 10.0
    random_seed: int = 42
