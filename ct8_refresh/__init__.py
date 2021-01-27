__version__ = '0.1.0'

import os
import sys
from pathlib import Path

from peewee import OperationalError, IntegrityError
from rich.console import Console
from ct8_refresh.cli import args


# Paths
root_path = Path(__file__).parent.parent
database_path = root_path / 'accounts.db'
logfile_path = root_path / 'run.log'


# Loguru and console initialization
mode = os.environ.get('MODE')
if mode == 'DEBUG' or args.debug:
    os.environ['LOGURU_LEVEL'] = 'DEBUG'
    print(f'Debug mode ON. Logging to: {logfile_path}')
else:
    os.environ['LOGURU_LEVEL'] = 'ERROR'

from loguru import logger
logger_config = {
    'handlers': [
        {
            'sink': logfile_path,
            'format': '{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {line} | {name}:{function} | {message}',
        },
        {
            'sink': sys.stderr,
            'format':   "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                        "<level>{level: <8}</level> | "
                        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            'diagnose': False,
            'level': 'ERROR',
        }
    ]
}
logger.configure(**logger_config)
console = Console()

from ct8_refresh.account.manager import AccountsManager
from ct8_refresh.account.views import AccountsView
from ct8_refresh.signin_loop import signin_loop


def handle_args():
    logger.debug(args)
    manager = AccountsManager()

    if args.command == 'run':
        if args.all or not args.all:
            signin_loop()

    if args.command == 'user':
        if args.add:
            for account in args.add:
                manager.add(account)
        if args.delete:
            for account in args.delete:
                manager.delete(account)

        if args.enable_account:
            for account in args.enable_account:
                manager.set_active(account, True)
        if args.disable_account:
            for account in args.disable_account:
                manager.set_active(account, False)

        if args.show_accounts:
            AccountsView.show_accounts()


@logger.catch(exclude=(OperationalError, IntegrityError))
def main():
    try:
        handle_args()
    except KeyboardInterrupt:
        sys.exit('\nInterrupted by user.')
