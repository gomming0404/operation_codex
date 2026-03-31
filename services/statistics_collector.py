from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class TimeWeightedMetric:
    last_time: float = 0.0
    last_value: float = 0.0
    weighted_sum: float = 0.0
    max_value: float = 0.0

    def observe(self, now: float, value: float) -> None:
        dt = now - self.last_time
        if dt > 0:
            self.weighted_sum += self.last_value * dt
        self.last_time = now
        self.last_value = value
        self.max_value = max(self.max_value, value)

    def avg(self, horizon: float) -> float:
        if horizon <= 0:
            return 0.0
        return self.weighted_sum / horizon


@dataclass
class StatisticsCollector:
    event_log: list[dict] = field(default_factory=list)
    content_metrics: dict[str, TimeWeightedMetric] = field(default_factory=lambda: defaultdict(TimeWeightedMetric))
    blocked_start: dict[str, float] = field(default_factory=dict)
    blocked_time: dict[str, float] = field(default_factory=lambda: defaultdict(float))
    lead_times: list[float] = field(default_factory=list)
    wip_metric: TimeWeightedMetric = field(default_factory=TimeWeightedMetric)

    def log(self, now: float, obj: str, event: str, mu_id: str | None = None, **data) -> None:
        rec = {"time": now, "object": obj, "event": event, "mu_id": mu_id}
        rec.update(data)
        self.event_log.append(rec)

    def observe_content(self, obj: str, now: float, value: int) -> None:
        self.content_metrics[obj].observe(now, value)

    def observe_wip(self, now: float, value: int) -> None:
        self.wip_metric.observe(now, value)

    def mark_block_start(self, obj: str, now: float) -> None:
        if obj not in self.blocked_start:
            self.blocked_start[obj] = now
            self.log(now, obj, "BLOCK_START")

    def mark_block_end(self, obj: str, now: float) -> None:
        if obj in self.blocked_start:
            self.blocked_time[obj] += now - self.blocked_start[obj]
            self.log(now, obj, "BLOCK_END")
            del self.blocked_start[obj]
