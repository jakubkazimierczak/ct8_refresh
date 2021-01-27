import os
import sys
from peewee import OperationalError, IntegrityError
from rich.console import Console
from ct8_refresh.cli import args


# Loguru and console initialization
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


def _real_main():
    # print(args)
    manager = AccountsManager()

    if args.debug:
        os.environ['MODE'] = 'DEBUG'

    if args.command == 'run':
        if not args.all:
            signin_loop()
        else:
            raise NotImplementedError('Signing-in to all account is not implemented yet.')

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
        _real_main()
    except KeyboardInterrupt:
        sys.exit('\nInterrupted by user.')
