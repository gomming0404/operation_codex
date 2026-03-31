import simpy
from model.store_object import StoreObject
from model.drain_object import DrainObject
from services.statistics_collector import StatisticsCollector


def store_to_drain_dispatch_process(
    env: simpy.Environment,
    store_obj: StoreObject,
    drain_obj: DrainObject,
    stats: StatisticsCollector,
    interval: float,
):
    while True:
        mu = yield store_obj.store.get()
        stats.observe_content(store_obj.object_id, env.now, store_obj.current_content)
        stats.log(env.now, store_obj.object_id, "LEAVE", mu.mu_id)
        yield env.timeout(interval)
        drain_obj.completed_count += 1
        stats.log(env.now, drain_obj.object_id, "DRAIN", mu.mu_id)
        lead_time = env.now - mu.created_time
        stats.lead_times.append(lead_time)
