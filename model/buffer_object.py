from dataclasses import dataclass
import simpy
from model.base import ModelObject


@dataclass
class BufferObject(ModelObject):
    store: simpy.Store
    capacity: int

    @property
    def current_content(self) -> int:
        return len(self.store.items)
