from dataclasses import dataclass, field


@dataclass
class MU:
    mu_id: str
    created_time: float
    timestamps: dict[str, float] = field(default_factory=dict)

    def mark(self, key: str, t: float) -> None:
        self.timestamps[key] = t
