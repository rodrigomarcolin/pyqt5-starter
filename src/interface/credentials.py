from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from src.lib.configmanager.configmanager import ConfigManager
from src.app.logger import get_logger

logger = get_logger(__name__)

SAVE_BUTTON_TEXT = "Salvar Credenciais"


class CredentialsTab(QMainWindow):
    def __init__(self, main_window):
        self.configmanager = ConfigManager()
        self.main_window = main_window

    def build(self):
        logger.info("Building WelcomeTab")
        self.tab = QWidget()
        self.tab.layout = QVBoxLayout(self.main_window)

        self._build_info()
        self._build_credentials_form()

        self.tab.setLayout(self.tab.layout)
        return self.tab

    def _build_info(self):
        info = QLabel(
            "<p>Exemplo de tela de cadastro de credenciais.</p>"
            "<p>As credenciais são salvas de maneira encriptada. Podem ser descriptografadas e utilizadas nas automações.</p>"
            f"<p>Preencha os campos abaixo e clique em '{SAVE_BUTTON_TEXT}'.</p>"
        )
        info.setWordWrap(True)
        self.tab.layout.addWidget(info)

    def _build_credentials_form(self):
        self._build_username_field()
        self._build_password_field()
        self._build_save_button()

    def _build_username_field(self):
        username_layout = QHBoxLayout()

        username_label = QLabel("Usuário:")
        username_layout.addWidget(username_label)

        self.username_edit = QLineEdit(self.configmanager.get("username"))
        username_layout.addWidget(self.username_edit)

        self.tab.layout.addLayout(username_layout)

    def _build_password_field(self):
        # Builds horizontal password input

        password_layout = QHBoxLayout()

        password_label = QLabel("Senha:")
        password_layout.addWidget(password_label)

        self.password_edit = QLineEdit(self.configmanager.get("password"))
        self.password_edit.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(self.password_edit)

        self.tab.layout.addLayout(password_layout)

    def _build_save_button(self):
        save_button = QPushButton(SAVE_BUTTON_TEXT)
        # When button is clicked, self.save_credentials() executes
        save_button.clicked.connect(lambda _: self.save_credentials())
        self.tab.layout.addWidget(save_button)

    def save_credentials(self):
        # Gets input from username_edit and password_edit, and
        # saves them with configmanager's helper function
        logger.info("Saving credentials...")
        self.configmanager.save_credentials(
            self.username_edit.text(), self.password_edit.text()
        )
        logger.info("Saved credentials")
