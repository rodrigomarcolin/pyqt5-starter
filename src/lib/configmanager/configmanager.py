from src.app import common
from src.lib.configmanager.configmanager_constants import (
    IS_FIRST_RUN,
    USERNAME,
    PASSWORD,
)
from PyQt5.QtCore import QSettings
from cryptography.fernet import Fernet
from src.app.logger import get_logger

logger = get_logger(__name__)

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ConfigManager(metaclass=SingletonMeta):
    """
    Singleton that contains all application configuration, and provides methods for updating and
    maintaining consistency of the configuration.

    Always encrypt everything using the secretkey.
    """

    """
    Static member for global application settings.
    """

    CLASS_VERSION = common.VERSION

    SETTINGS = {
        IS_FIRST_RUN: True,
    }

    def __init__(self):
        self.VERSION = self.__class__.CLASS_VERSION
        self.settings = QSettings(common.COMPANY_NAME, common.APP_NAME)

        # Encryption - For storing user credentials
        self.secret_key = self.__get_or_create_secret()
        self.cipher_suite = Fernet(self.secret_key)

    def save(self, name, value):
        self.settings.setValue(name, self.encrypt(value))

    def get(self, setting):
        value = self.settings.value(setting, "")
        try:
            return self.cipher_suite.decrypt(value).decode()
        except:
            logger.info("Could not decrypt")
            return ""

    # Helper functions
    def save_credentials(self, username, password):
        self.save(USERNAME, username)
        self.save(PASSWORD, password)

        logger.info("Credentials saved.")

    def get_credentials(self):
        return {
            USERNAME: self.get(USERNAME),
            PASSWORD: self.get(PASSWORD),
        }

    def encrypt(self, data: str):
        return self.cipher_suite.encrypt(data.encode())

    def __get_or_create_secret(self):
        secret_key = self.settings.value("secret_key")
        if secret_key is None:
            logger.info("No secret key found - creating new one")
            secret_key = Fernet.generate_key()
            self.settings.setValue("secret_key", secret_key)
        else:
            secret_key = bytes(secret_key)
        return secret_key
