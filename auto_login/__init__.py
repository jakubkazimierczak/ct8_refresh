import os
import sys
from peewee import OperationalError, IntegrityError
from rich.console import Console
from auto_login.cli import args
from auto_login.account.manager import AccountsManager
from auto_login.signin_loop import signin_loop


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


def _real_main():
    manager = AccountsManager()

    if args.debug:
        os.environ['MODE'] = 'DEBUG'

    if args.run:
        signin_loop()

    if args.add_account:
        for account in args.add_account:
            manager.add(account)
    if args.del_account:
        for account in args.del_account:
            manager.delete(account)

    if args.enable_account:
        for account in args.enable_account:
            manager.enable(account)
    if args.disable_account:
        for account in args.disable_account:
            manager.disable(account)


@logger.catch(exclude=(OperationalError, IntegrityError))
def main():
    try:
        from auto_login import __main__
    except KeyboardInterrupt:
        sys.exit('\nInterrupted by user.')
