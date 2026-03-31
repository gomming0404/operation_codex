import simpy
from domain.mu import MU
from model.source_object import SourceObject
from model.conveyor_object import ConveyorObject
from services.distribution_service import DistributionService
from services.statistics_collector import StatisticsCollector


def source_generation_process(
    env: simpy.Environment,
    source: SourceObject,
    conveyor: ConveyorObject,
    distribution: DistributionService,
    stats: StatisticsCollector,
    simulation_time: float,
):
    idx = 0
    while env.now < simulation_time:
        dt = distribution.sample_non_negative_normal(7.0, 5.0)
        if env.now + dt > simulation_time:
            break
        yield env.timeout(dt)
        mu = MU(mu_id=f"MU_{idx:06d}", created_time=env.now)
        mu.mark("source_exit", env.now)
        source.generated_count += 1
        idx += 1
        stats.log(env.now, source.object_id, "GENERATE", mu.mu_id)
        env.process(conveyor_transfer_process(env, conveyor, mu, stats))


def conveyor_transfer_process(env: simpy.Environment, conveyor: ConveyorObject, mu: MU, stats: StatisticsCollector):
    conveyor.in_transit += 1
    stats.log(env.now, conveyor.object_id, "ENTER", mu.mu_id)
    yield env.timeout(conveyor.transfer_time)
    conveyor.in_transit -= 1
    stats.log(env.now, conveyor.object_id, "EXIT", mu.mu_id)
