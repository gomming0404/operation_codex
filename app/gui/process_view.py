from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPen


class ProcessViewWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.anchor_data = {}
        self.state = {}

    def set_anchor_data(self, anchor_data: dict) -> None:
        self.anchor_data = anchor_data
        self.update()

    def set_state(self, state: dict) -> None:
        self.state = state
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor("white"))
        painter.setPen(QPen(QColor("black"), 2))

        objects = self.anchor_data.get("objects", [])
        by_id = {o["id"]: o for o in objects}
        for conn in self.anchor_data.get("connections", []):
            f = by_id.get(conn["from"])
            t = by_id.get(conn["to"])
            if not f or not t:
                continue
            fx, fy = f["anchors"].get("exit", f["position"])["x"], f["anchors"].get("exit", f["position"])["y"]
            tx, ty = t["anchors"].get("entrance", t["position"])["x"], t["anchors"].get("entrance", t["position"])["y"]
            painter.drawLine(fx, fy, tx, ty)

        for obj in objects:
            x = obj["position"]["x"] - 35
            y = obj["position"]["y"] - 20
            painter.drawRect(x, y, 70, 40)
            txt = f"{obj['id']}\n{self.state.get(obj['id'], '')}"
            painter.drawText(x + 3, y + 15, txt)
