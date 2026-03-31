import simpy
from domain.worker import Worker
from model.buffer_object import BufferObject
from model.store_object import StoreObject
from services.statistics_collector import StatisticsCollector


def worker_transport_process(
    env: simpy.Environment,
    worker: Worker,
    buffer_obj: BufferObject,
    store_obj: StoreObject,
    stats: StatisticsCollector,
    distance_m: float,
):
    while True:
        worker.set_state("PICKING")
        mu = yield buffer_obj.store.get()
        stats.observe_content(buffer_obj.object_id, env.now, buffer_obj.current_content)
        stats.log(env.now, buffer_obj.object_id, "LEAVE", mu.mu_id)

        worker.current_mu = mu
        worker.set_state("WALKING")
        worker.walk_distance += distance_m
        yield env.timeout(worker.move_time(distance_m))

        worker.set_state("DROPPING")
        yield store_obj.store.put(mu)
        mu.mark("store_enter", env.now)
        worker.task_count += 1
        stats.observe_content(store_obj.object_id, env.now, store_obj.current_content)
        stats.log(env.now, store_obj.object_id, "ENTER", mu.mu_id)
        worker.current_mu = None
        worker.set_state("IDLE")
