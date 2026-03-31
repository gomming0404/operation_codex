import simpy
from domain.worker import Worker


class WorkerPool:
    def __init__(self, env: simpy.Environment, workers: list[Worker]):
        self.env = env
        self.workers = workers
        self.resource = simpy.Resource(env, capacity=len(workers))

    def get_single_worker(self) -> Worker:
        return self.workers[0]
