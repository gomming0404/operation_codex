from dataclasses import dataclass
from domain.anchor import AnchorPoint


@dataclass
class WorkerPlace:
    place_id: str
    waiting_position: AnchorPoint
