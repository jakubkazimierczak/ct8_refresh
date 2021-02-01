import sys

from loguru import logger

from . import LOG_PATH


class Loggers:
    def __init__(self, debug_switch=None):
        self.file_handler_id = None
        self.stderr_handler_id = None

        # Initialise loggers
        logger.remove()  # Disable default logger
        if debug_switch:
            self.add_file_logger(level='DEBUG')
        else:
            self.add_file_logger()
        self.add_stderr()

    def add_file_logger(self, level='ERROR'):
        self.file_handler_id = logger.add(
            LOG_PATH,
            format='{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {line} | {name}:{function} | {message}',
            level=level,
        )
        return self.file_handler_id

    def add_stderr(self, level='WARNING'):
        self.stderr_handler_id = logger.add(
            sys.stderr,
            format='<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | '
            '<level>{level: <8}</level> | '
            '<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>',
            diagnose=False,
            level=level,
        )
        return self.stderr_handler_id
