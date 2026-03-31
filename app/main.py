import sys
from pathlib import Path

# Conflict-resolution note:
# Support both execution styles used by reviewers/CI.
# - python -m app.main (package mode)
# - python app/main.py (script mode)
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PySide6.QtWidgets import QApplication
from app.gui.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1500, 900)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
