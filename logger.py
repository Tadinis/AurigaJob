from dataclasses import dataclass
import logging
import os
import sys
import datetime

class Logger:
    """Logger which logs oui_data_for_scanner into file and console"""

    _logger = None
    date = datetime.datetime.now()
    suffix = date.strftime("%Y-%m-%d")
    root_dir = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, filename, file_level=logging.INFO, console_level=logging.INFO, mode='w'):
        self.filename = ''.join([self.suffix, "_", filename, ".txt"])
        self.logging_path = os.sep.join([self.root_dir, self.filename])
        # Creating logger
        self.__class__._logger = logging.getLogger("Logging")
        self.__class__._logger.level = logging.DEBUG
        # Creating file and console handlers
        self.file_handler = logging.FileHandler(filename=self.logging_path, mode=mode)
        self.file_handler.setLevel(level=file_level)
        self.console_handler = logging.StreamHandler(stream=sys.stdout)
        self.console_handler.setLevel(level=console_level)

        # Create formatter and add it to the handler
        self.file_format = logging.Formatter(
            "%(asctime)s__%(name)s__%(levelname)s__%(message)s", "%H:%M:%S")
        self.console_format = logging.Formatter(
            "%(asctime)s__%(name)s__%(levelname)s__%(message)s", "%H:%M:%S")
        self.file_handler.setFormatter(self.file_format)
        self.console_handler.setFormatter(self.console_format)

        # Add the handlers to the logger
        self._logger.addHandler(self.file_handler)
        self._logger.addHandler(self.console_handler)

    @staticmethod
    def info(msg):
        Logger._logger.info(msg)

    @staticmethod
    def warning(msg):
        Logger._logger.warning(msg)

    @staticmethod
    def error(msg):
        Logger._logger.error(msg)

    @staticmethod
    def critical(msg):
        Logger._logger.critical(msg)

    @staticmethod
    def debug(msg):
        Logger._logger.debug(msg)
