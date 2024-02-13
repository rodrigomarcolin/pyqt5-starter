import logging
import logging.handlers
import pathlib
import sys
from src.app.common import APP_NAME, DATA_DIR


# Logger module

root_logger = logging.getLogger(APP_NAME)

MAX_LOG_SIZE = 5 * 2**20  # 5 megabytes
MAX_LOG_COUNT = 3
LOG_FORMAT = "%(asctime)s %(levelname)s - %(name)s - %(message)s"
LOG_FILE = pathlib.Path(DATA_DIR) / f"{APP_NAME}.log"


def get_logger(full_module_path: str) -> logging.Logger:
    module_path = ".".join(full_module_path.split(".")[1:])
    return root_logger.getChild(module_path)


def configure_root_logger(verbose=False):
    """Initialise logging system"""
    root_logger.setLevel(1)
    pathlib.Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE, maxBytes=MAX_LOG_SIZE, backupCount=MAX_LOG_COUNT
    )
    file_handler.setLevel(logging.INFO)

    stdout_stream_handler = logging.StreamHandler(sys.stdout)
    logging_level = logging.INFO
    if verbose:
        logging_level = logging.DEBUG

    stdout_stream_handler.setLevel(logging_level)
    stdout_stream_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    root_logger.addHandler(stdout_stream_handler)
    root_logger.addHandler(file_handler)
