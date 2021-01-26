import argparse
import os
from auto_login.account.manager import AccountsManager
from auto_login.signin_loop import signin_loop


parser = argparse.ArgumentParser()
parser.add_argument(
    '--debug',
    action='store_true',
    help='Toggle debug mode on.'
)
parser.add_argument(
    '-a', '--add-account',
    action='store',
    nargs='+',
    help='Add account to DB.',
    metavar='login',
)
parser.add_argument(
    '--del-account',
    action='store',
    nargs='+',
    help='Delete account from DB.',
    metavar='login',
)
parser.add_argument(
    '-e', '--enable-account',
    action='store',
    nargs='+',
    help='Enable account to automatic sign-in.',
    metavar='login',
)
parser.add_argument(
    '-d', '--disable-account',
    action='store',
    nargs='+',
    help='Disable account from automatic sign-in.',
    metavar='login',
)
parser.add_argument(
    '-r', '--run',
    action='store_true',
    help='Sign-in to enabled accounts.'
)
args = parser.parse_args()


manager = AccountsManager()
if args.debug:
    os.environ['MODE'] = 'DEBUG'

if args.run:
    app()

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
