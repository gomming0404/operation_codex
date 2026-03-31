from dataclasses import dataclass
from model.base import ModelObject


@dataclass
class DrainObject(ModelObject):
    completed_count: int = 0
