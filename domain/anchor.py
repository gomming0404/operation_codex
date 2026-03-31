from dataclasses import dataclass, field


@dataclass(frozen=True)
class AnchorPoint:
    x: float
    y: float


@dataclass
class AnchorSet:
    object_id: str
    object_type: str
    position: AnchorPoint
    anchors: dict[str, AnchorPoint] = field(default_factory=dict)

    def get(self, name: str) -> AnchorPoint:
        if name not in self.anchors:
            raise KeyError(f"Anchor '{name}' missing for object '{self.object_id}'")
        return self.anchors[name]
