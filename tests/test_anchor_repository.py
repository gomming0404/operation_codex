import json
import pytest
from pathlib import Path
from services.anchor_repository import AnchorRepository


def test_anchor_load_and_get(anchor_json_path):
    repo = AnchorRepository(anchor_json_path)
    repo.load()
    aset = repo.get_anchor_set("BUF_01")
    assert aset.get("entrance").x == 9
    assert aset.get("worker_pickup").y == 1


def test_anchor_validation_error(tmp_path: Path):
    p = tmp_path / "bad.json"
    p.write_text(json.dumps({"objects": [{"id": "A"}]}), encoding="utf-8")
    repo = AnchorRepository(str(p))
    with pytest.raises(ValueError):
        repo.load()
