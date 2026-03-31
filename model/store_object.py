from dataclasses import dataclass
import simpy
from model.base import ModelObject


@dataclass
class StoreObject(ModelObject):
    store: simpy.Store

    @property
    def current_content(self) -> int:
        return len(self.store.items)
