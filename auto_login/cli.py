import argparse


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()


# -----------------------------------------------
# Main parser
# -----------------------------------------------
parser.add_argument(
    '--debug',
    action='store_true',
    help='toggle debug mode on'
)


# -----------------------------------------------
# Users parser
# -----------------------------------------------
user_parser = subparsers.add_parser('user', help='Manage user account(s)')
user_parser.add_argument(
    '-a', '--add-account',
    action='store',
    nargs='+',
    help='add account to DB',
    metavar='login',
)
user_parser.add_argument(
    '--del-account',
    action='store',
    nargs='+',
    help='delete account from DB',
    metavar='login',
)
user_parser.add_argument(
    '-e', '--enable-account',
    action='store',
    nargs='+',
    help='enable account to automatic sign-in',
    metavar='login',
)
user_parser.add_argument(
    '-d', '--disable-account',
    action='store',
    nargs='+',
    help='disable account from automatic sign-in',
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
