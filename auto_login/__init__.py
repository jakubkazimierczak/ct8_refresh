import os
import sys
from rich.console import Console

# Loguru configuration
mode = os.environ.get('MODE')
if mode == 'DEBUG':
    os.environ['LOGURU_LEVEL'] = 'DEBUG'
else:
    os.environ['LOGURU_LEVEL'] = 'WARNING'

from loguru import logger
logger_config = {
    'handlers': [
        {
            'sink': 'run.log',
            'format': '{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {line} | {name}:{function} | {message}'
        },
        # {
        #     'sink': sys.stderr,
        #     'format':   "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        #                 "<level>{level: <8}</level> | "
        #                 "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        #     'diagnose': False
        # }
    ]
}
logger.configure(**logger_config)

console = Console()
