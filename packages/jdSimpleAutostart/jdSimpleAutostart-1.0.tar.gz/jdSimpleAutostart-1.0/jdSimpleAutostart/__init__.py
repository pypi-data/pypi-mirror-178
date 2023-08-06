from PyQt6.QtCore import QTranslator, QLocale, QLibraryInfo, QCoreApplication
from .Functions import get_system_autostart_path, get_user_autostart_path
from PyQt6.QtWidgets import QApplication, QMessageBox
from .MainWindow import MainWindow
from PyQt6.QtGui import QIcon
import sys
import os


def main():
    app = QApplication(sys.argv)

    qt_translator = QTranslator()
    app_translator = QTranslator()
    system_language = QLocale.system().name().split("_")[0]
    qt_translator.load(os.path.join(QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath), "qt_" + system_language + ".qm"))
    app_translator.load(os.path.join(os.path.dirname(__file__), "translations", "jdSimpleAutostart_" + system_language + ".qm"))
    app.installTranslator(app_translator)
    app.installTranslator(qt_translator)

    if not os.path.isdir(get_system_autostart_path()) and not os.path.isdir(get_user_autostart_path()):
        QMessageBox.critical(None, QCoreApplication.translate("jdSimpleAutostart", "No autostart directories found"), QCoreApplication.translate("jdSimpleAutostart", "No autostart directories were found. Maybe your Desktop Environment don't support the autostart specification."))
        sys.exit(0)

    icon = QIcon(os.path.join(os.path.dirname(__file__), "Icon.svg"))
    app.setWindowIcon(icon)

    w = MainWindow(icon)
    w.show()

    sys.exit(app.exec())
