from dataclasses import dataclass, field
from typing import Optional
import simpy

from domain.mu import MU
from domain.worker_place import WorkerPlace


@dataclass
class Worker:
    worker_id: str
    speed_mps: float
    env: simpy.Environment
    home_place: WorkerPlace
    state: str = "IDLE"
    task_count: int = 0
    busy_time: float = 0.0
    waiting_time: float = 0.0
    walk_distance: float = 0.0
    last_state_change_time: float = 0.0
    current_mu: Optional[MU] = None
    state_history: list[tuple[float, str]] = field(default_factory=list)

    def set_state(self, new_state: str) -> None:
        now = self.env.now
        elapsed = now - self.last_state_change_time
        if self.state == "IDLE":
            self.waiting_time += max(0.0, elapsed)
        else:
            self.busy_time += max(0.0, elapsed)
        self.state = new_state
        self.last_state_change_time = now
        self.state_history.append((now, new_state))

    def move_time(self, distance: float) -> float:
        return distance / self.speed_mps
