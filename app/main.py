import sys
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
