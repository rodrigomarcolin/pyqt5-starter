import os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from src.app.common import BASE_DIR, DATA_DIR, APP_NAME, VERSION
from src.interface.credentials import CredentialsTab
from src.interface.welcome import WelcomeTab
from src.lib.configmanager.configmanager import ConfigManager
from src.app.logger import get_logger, configure_root_logger
from typing import Union


logger = get_logger(__name__)


# Setup Application
class Application:
    def __init__(self):
        self.setup_dirs()

    @staticmethod
    def setup_dirs():
        dirs = [BASE_DIR, DATA_DIR]
        for directory in dirs:
            if not os.path.exists(directory):
                os.makedirs(directory)


# Application's main window
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setup_main_window()

        # Defines which tabs to render
        self.tabs = {
            "Início": WelcomeTab(
                self
            ).build(),  # Each tab knows how to render itself. All logic is self-contained
            "Credentials": CredentialsTab(self).build(),
        }

        self.setup_tabs()

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
        self.threadpool = QThreadPool()

    def setup_main_window(self):
        configure_root_logger(True)
        self.configmanager = ConfigManager()
        self.setWindowTitle(f"{APP_NAME} - {VERSION}")
        self.layout = QVBoxLayout()

    def setup_tabs(self):
        self.tabs_widget = QTabWidget()
        self.layout.addWidget(self.tabs_widget)
        for nome, tab in self.tabs.items():
            self.tabs_widget.addTab(tab, nome)

    def show_success_message(self, message):
        QMessageBox.information(self, "Success", message)

    def show_error_message(self, error_message):
        QMessageBox.critical(self, "Error", error_message)


app = QApplication([])
window = MainWindow()
window.resize(300, 300)
window.show()
app.exec_()
