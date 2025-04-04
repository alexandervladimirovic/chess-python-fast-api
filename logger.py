import datetime
import json
import logging
import os
from logging import Logger
from logging.handlers import RotatingFileHandler


class JSONFormatter(logging.Formatter):
    """Custom formatter for logging in JSON format.

    Class inherits from logging.Formatter and overrides the format method,
    format log messages into a JSON structure with additional information
    about time, logging level, messages, logger, file, and string.
    """

    def format(self, record):
        """Formats log message into JSON string.

        :param record: log recording object (logging.LogRecord).
        :return: String in JSON format with information about log.
        """
        log_obj = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "file": os.path.basename(record.pathname),
            "line": record.lineno,
        }
        return json.dumps(log_obj)


def setup_logging() -> Logger:
    """SetUp logging."""
    directory = "logs"

    if not os.path.exists(directory):
        os.makedirs(directory)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # SetUp file
    file_name = f"{datetime.datetime.now(tz=datetime.UTC).strftime('%Y-%m-%d')}.log"
    file_path = os.path.join(directory, file_name)
    file_handler = RotatingFileHandler(
        file_path, maxBytes=1024 * 1024 * 10, backupCount=5
    )
    file_handler.setFormatter(JSONFormatter())
    logger.addHandler(file_handler)

    # SetUp console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(JSONFormatter())
    logger.addHandler(console_handler)

    return logger
