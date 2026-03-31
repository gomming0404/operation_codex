from dataclasses import dataclass
import simpy

from config.scenario_config import ScenarioConfig
from domain.worker import Worker
from domain.worker_place import WorkerPlace
from domain.worker_pool import WorkerPool
from model.source_object import SourceObject
from model.conveyor_object import ConveyorObject
from model.buffer_object import BufferObject
from model.store_object import StoreObject
from model.drain_object import DrainObject
from process.worker_transport_process import worker_transport_process
from process.store_dispatch_process import store_to_drain_dispatch_process
from services.distribution_service import DistributionService
from services.statistics_collector import StatisticsCollector
from services.anchor_repository import AnchorRepository


@dataclass
class SimulationModel:
    env: simpy.Environment
    config: ScenarioConfig
    source: SourceObject
    conveyor: ConveyorObject
    buffer: BufferObject
    store: StoreObject
    drain: DrainObject
    worker_pool: WorkerPool
    worker_01: Worker
    stats: StatisticsCollector
    distribution: DistributionService

    def run(self, until: float | None = None) -> None:
        self.env.run(until=until or self.config.simulation_time)
        # finalize state durations
        self.worker_01.set_state(self.worker_01.state)


class RuntimeModelBuilder:
    def __init__(self, anchor_repo: AnchorRepository):
        self.anchor_repo = anchor_repo

    def build(self, config: ScenarioConfig, distribution: DistributionService | None = None) -> SimulationModel:
        env = simpy.Environment()
        stats = StatisticsCollector()
        distribution = distribution or DistributionService(config.random_seed)

        source = SourceObject("SRC_01", "Source", self.anchor_repo.get_anchor_set("SRC_01"))
        conveyor = ConveyorObject("CONV_01", "Conveyor", self.anchor_repo.get_anchor_set("CONV_01"), config.conveyor_length, config.conveyor_speed)
        buffer_obj = BufferObject("BUF_01", "Buffer", self.anchor_repo.get_anchor_set("BUF_01"), simpy.Store(env, capacity=config.buffer_capacity), config.buffer_capacity)
        store = StoreObject("STORE_01", "Store", self.anchor_repo.get_anchor_set("STORE_01"), simpy.Store(env))
        drain = DrainObject("DRAIN_01", "Drain", self.anchor_repo.get_anchor_set("DRAIN_01"))

        place_anchor = self.anchor_repo.get_anchor_set("WORKER_PLACE_01").get("waiting_position")
        worker_place = WorkerPlace("WORKER_PLACE_01", place_anchor)
        worker = Worker("WORKER_01", config.worker_01_speed, env, worker_place)
        pool = WorkerPool(env, [worker])

        env.process(self._source_to_conveyor_to_buffer(env, config, source, conveyor, buffer_obj, distribution, stats))
        env.process(worker_transport_process(env, worker, buffer_obj, store, stats, config.buffer_to_store_distance))
        env.process(store_to_drain_dispatch_process(env, store, drain, stats, config.store_dispatch_interval))

        return SimulationModel(env, config, source, conveyor, buffer_obj, store, drain, pool, worker, stats, distribution)

    def _source_to_conveyor_to_buffer(self, env, config, source, conveyor, buffer_obj, distribution, stats):
        i = 0
        while env.now < config.simulation_time:
            dt = distribution.sample_non_negative_normal(config.mu_interarrival_mean, config.mu_interarrival_std)
            if env.now + dt > config.simulation_time:
                break
            yield env.timeout(dt)
            from domain.mu import MU
            mu = MU(f"MU_{i:06d}", env.now)
            i += 1
            source.generated_count += 1
            stats.log(env.now, source.object_id, "GENERATE", mu.mu_id)
            stats.observe_wip(env.now, source.generated_count - self._completed_count_estimate(stats))
            # Conveyor(Line)
            conveyor.in_transit += 1
            stats.log(env.now, conveyor.object_id, "ENTER", mu.mu_id)
            yield env.timeout(conveyor.transfer_time)
            conveyor.in_transit -= 1
            # Buffer blocking semantics
            if buffer_obj.current_content >= buffer_obj.capacity:
                stats.mark_block_start(conveyor.object_id, env.now)
            while buffer_obj.current_content >= buffer_obj.capacity:
                yield env.timeout(0.1)
            stats.mark_block_end(conveyor.object_id, env.now)
            yield buffer_obj.store.put(mu)
            mu.mark("buffer_enter", env.now)
            stats.observe_content(buffer_obj.object_id, env.now, buffer_obj.current_content)
            stats.log(env.now, buffer_obj.object_id, "ENTER", mu.mu_id)

    def _completed_count_estimate(self, stats: StatisticsCollector) -> int:
        return len(stats.lead_times)
