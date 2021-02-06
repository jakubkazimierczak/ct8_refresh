import sys

from .cli import parser

args = parser.parse_args()

from loguru import logger
from .loggers import Loggers

Loggers(args.debug)

from . import LOG_PATH
from .account.manager import AccountsManager
from .account.views import AccountsView
from .run import Run


def handle_args():
    if args.debug_paths:
        print(f'Logfile path: {LOG_PATH}')

    if args.command == 'run':
        Run(args.all).main()

    if args.command == 'user':
        if args.add:
            for account in args.add:
                AccountsManager.add(account)
        if args.delete:
            for account in args.delete:
                AccountsManager.delete(account)

        if args.enable_account:
            for account in args.enable_account:
                AccountsManager.set_active(account, True)
        if args.disable_account:
            for account in args.disable_account:
                AccountsManager.set_active(account, False)

        if args.show_accounts:
            accounts = AccountsManager.get_all_accounts_sorted()
            AccountsView.show_accounts(accounts)


@logger.catch
def main():
    try:
        handle_args()
    except KeyboardInterrupt:
        sys.exit('\nInterrupted by user.')


if __name__ == '__main__':
    main()
