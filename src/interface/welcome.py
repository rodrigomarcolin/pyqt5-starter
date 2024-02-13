from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from src.lib.configmanager.configmanager import ConfigManager
from src.app.logger import get_logger
from src.app import common

logger = get_logger(__name__)


class WelcomeTab(QMainWindow):
    def __init__(self, main_window):
        self.configmanager = ConfigManager()
        self.main_window = main_window

    def build(self):
        logger.info('Building WelcomeTab')
        self.setup_tab()
        self.display_welcome()
        self.display_authors(common.AUTHORS)

        self.tab.setLayout(self.tab_layout)
        return self.tab

    def setup_tab(self):
        self.tab = QWidget()
        self.tab_layout = QVBoxLayout(self.main_window)

    def display_welcome(self):
        welcome_label = QLabel(
            f"<h2>Bem-vindo(a) ao {common.APP_NAME} {common.VERSION}!</h2>"
        )
        welcome_label.setAlignment(Qt.AlignCenter)
        self.tab_layout.addWidget(welcome_label)

    def display_authors(self, authors):
        # Header
        authors_label = QLabel("<h3>Autores:</h3>")
        authors_label.setAlignment(Qt.AlignCenter)
        self.tab_layout.addWidget(authors_label)

        # Author List
        for author in authors:
            author_label = QLabel(
                f"<p><b>{author['name']}</b><br>{author['email']}</p>"
            )
            author_label.setAlignment(Qt.AlignCenter)
            self.tab_layout.addWidget(author_label)
