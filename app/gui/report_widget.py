from PySide6.QtWidgets import QTextEdit


class ReportWidget(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)

    def set_report(self, object_report: dict, integrated_report: dict) -> None:
        lines = ["[Object Report]"]
        for obj, data in object_report.items():
            lines.append(f"- {obj}: {data}")
        lines.append("\n[Integrated Report]")
        for k, v in integrated_report.items():
            lines.append(f"- {k}: {v}")
        self.setPlainText("\n".join(lines))
