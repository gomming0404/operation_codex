from dataclasses import dataclass
from model.base import ModelObject


@dataclass
class SourceObject(ModelObject):
    generated_count: int = 0
