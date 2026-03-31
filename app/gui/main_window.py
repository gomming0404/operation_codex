from pathlib import Path
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog
)

from config.scenario_config import ScenarioConfig
from services.anchor_repository import AnchorRepository
from services.runtime_model_builder import RuntimeModelBuilder
from services.report_builder import ReportBuilder
from app.gui.process_view import ProcessViewWidget
from app.gui.event_log_widget import EventLogWidget
from app.gui.report_widget import ReportWidget


class SimThread(QThread):
    completed = Signal(object)

    def __init__(self, model):
        super().__init__()
        self.model = model

    def run(self):
        self.model.run()
        self.completed.emit(self.model)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Plant Simulation Style DES Tool")
        self.anchor_path = str(Path("config/anchors.json"))
        self.anchor_repo = None
        self.model = None
        self.thread = None

        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)

        cfg_row = QHBoxLayout()
        self.inputs = {}
        for key, val in ScenarioConfig().__dict__.items():
            cfg_row.addWidget(QLabel(key))
            le = QLineEdit(str(val))
            self.inputs[key] = le
            cfg_row.addWidget(le)
        layout.addLayout(cfg_row)

        ctl = QHBoxLayout()
        self.btn_load = QPushButton("Load Anchor JSON")
        self.btn_build = QPushButton("Build Model")
        self.btn_run = QPushButton("Run")
        self.btn_reset = QPushButton("Reset")
        ctl.addWidget(self.btn_load)
        ctl.addWidget(self.btn_build)
        ctl.addWidget(self.btn_run)
        ctl.addWidget(self.btn_reset)
        layout.addLayout(ctl)

        self.status_lbl = QLabel("Ready")
        layout.addWidget(self.status_lbl)

        self.process_view = ProcessViewWidget()
        self.process_view.setMinimumHeight(320)
        layout.addWidget(self.process_view)

        self.event_widget = EventLogWidget()
        layout.addWidget(self.event_widget)

        self.report_widget = ReportWidget()
        layout.addWidget(self.report_widget)

        self.btn_load.clicked.connect(self.load_anchor)
        self.btn_build.clicked.connect(self.build_model)
        self.btn_run.clicked.connect(self.run_model)
        self.btn_reset.clicked.connect(self.reset)

    def load_anchor(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Anchor JSON", self.anchor_path, "JSON (*.json)")
        if path:
            self.anchor_path = path
        self.anchor_repo = AnchorRepository(self.anchor_path)
        self.anchor_repo.load()
        self.process_view.set_anchor_data(self.anchor_repo.raw_data)
        self.status_lbl.setText(f"Anchor loaded: {self.anchor_path}")

    def _scenario(self) -> ScenarioConfig:
        kwargs = {}
        base = ScenarioConfig()
        for k, le in self.inputs.items():
            t = type(getattr(base, k))
            kwargs[k] = t(float(le.text())) if t is int else t(le.text())
        return ScenarioConfig(**kwargs)

    def build_model(self):
        if self.anchor_repo is None:
            self.anchor_repo = AnchorRepository(self.anchor_path)
            self.anchor_repo.load()
        builder = RuntimeModelBuilder(self.anchor_repo)
        self.model = builder.build(self._scenario())
        self.status_lbl.setText("Model built")

    def run_model(self):
        if self.model is None:
            self.build_model()
        self.thread = SimThread(self.model)
        self.thread.completed.connect(self._on_completed)
        self.thread.start()
        self.status_lbl.setText("Running...")

    def _on_completed(self, model):
        self.status_lbl.setText(f"Completed @ t={model.env.now:.2f}, drain={model.drain.completed_count}")
        self.event_widget.set_events(model.stats.event_log)
        obj = ReportBuilder.object_report(model.stats, model.config.simulation_time)
        integ = ReportBuilder.integrated_report(model.stats, model.config.simulation_time, model.drain.completed_count, model.worker_01.busy_time)
        self.report_widget.set_report(obj, integ)
        state = {
            "SRC_01": f"gen={model.source.generated_count}",
            "CONV_01": f"in_transit={model.conveyor.in_transit}",
            "BUF_01": f"content={model.buffer.current_content}",
            "STORE_01": f"content={model.store.current_content}",
            "DRAIN_01": f"done={model.drain.completed_count}",
            "WORKER_PLACE_01": f"worker={model.worker_01.state}/task={model.worker_01.task_count}",
        }
        self.process_view.set_state(state)

    def reset(self):
        self.model = None
        self.event_widget.setRowCount(0)
        self.report_widget.setPlainText("")
        self.status_lbl.setText("Reset")
        # TODO: Pause/Resume 구현 시 스레드 상태 초기화 로직 확장
