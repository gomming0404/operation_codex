from PySide6.QtWidgets import QTableWidget, QTableWidgetItem


class EventLogWidget(QTableWidget):
    def __init__(self):
        super().__init__(0, 4)
        self.setHorizontalHeaderLabels(["time", "object", "event", "mu_id"])

    def set_events(self, events: list[dict]) -> None:
        self.setRowCount(0)
        for rec in events[-200:]:
            row = self.rowCount()
            self.insertRow(row)
            self.setItem(row, 0, QTableWidgetItem(f"{rec.get('time', 0):.2f}"))
            self.setItem(row, 1, QTableWidgetItem(str(rec.get("object", ""))))
            self.setItem(row, 2, QTableWidgetItem(str(rec.get("event", ""))))
            self.setItem(row, 3, QTableWidgetItem(str(rec.get("mu_id", ""))))
