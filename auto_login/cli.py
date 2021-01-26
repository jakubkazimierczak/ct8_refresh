import argparse


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()


# -----------------------------------------------
# Main parser
# -----------------------------------------------
parser.add_argument(
    '--debug',
    action='store_true',
    help='Toggle debug mode on.'
)


# -----------------------------------------------
# Users parser
# -----------------------------------------------
users_parser = subparsers.add_parser('user', help='Manage user account(s)')
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


# -----------------------------------------------
# Run parser
# -----------------------------------------------
run_parser = subparsers.add_parser('run', help='Run automatic sign-in')
run_parser.add_argument(
    '--all',
    action='store_true',
    default=False,
    help='try sign-in to all (even disabled) accounts'
)


args = parser.parse_args()
