import sys
from pathlib import Path

# Allow both execution modes:
# 1) python -m app.main
# 2) python app/main.py
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PySide6.QtWidgets import QApplication
from app.gui.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    w = MainWindow()
    w.resize(1500, 900)
    w.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
