import json
from pathlib import Path
from domain.anchor import AnchorPoint, AnchorSet


class AnchorRepository:
    def __init__(self, path: str):
        self.path = Path(path)
        self._objects: dict[str, AnchorSet] = {}
        self.raw_data: dict = {}

    def load(self) -> None:
        self.raw_data = json.loads(self.path.read_text(encoding='utf-8'))
        objs = self.raw_data.get("objects")
        if not isinstance(objs, list):
            raise ValueError("Invalid anchor JSON: 'objects' must be a list")
        parsed: dict[str, AnchorSet] = {}
        for obj in objs:
            if "id" not in obj or "type" not in obj or "anchors" not in obj or "position" not in obj:
                raise ValueError("Invalid object anchor spec")
            anchors = {k: AnchorPoint(v["x"], v["y"]) for k, v in obj["anchors"].items()}
            parsed[obj["id"]] = AnchorSet(
                object_id=obj["id"],
                object_type=obj["type"],
                position=AnchorPoint(obj["position"]["x"], obj["position"]["y"]),
                anchors=anchors,
            )
        self._objects = parsed

    def get_anchor_set(self, object_id: str) -> AnchorSet:
        if object_id not in self._objects:
            raise KeyError(f"Object ID not found: {object_id}")
        return self._objects[object_id]
