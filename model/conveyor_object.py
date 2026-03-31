from dataclasses import dataclass
from model.base import ModelObject


@dataclass
class ConveyorObject(ModelObject):
    length_m: float
    speed_mps: float
    in_transit: int = 0

    @property
    def transfer_time(self) -> float:
        return self.length_m / self.speed_mps
