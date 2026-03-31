from dataclasses import dataclass
from domain.anchor import AnchorSet


@dataclass
class ModelObject:
    object_id: str
    object_type: str
    anchor_set: AnchorSet
