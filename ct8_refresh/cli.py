import argparse
import textwrap


parser = argparse.ArgumentParser(
    prog='ct8_refresh',
    usage='%(prog)s [options]'
)
subparsers = parser.add_subparsers(dest='command')


# -----------------------------------------------
# Main parser
# -----------------------------------------------
parser.add_argument(
    '--debug',
    action='store_true',
    help='toggle debug mode on'
)
parser.add_argument(
    '--debug-paths',
    action='store_true',
    help='show path where debug information is stored'
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


# -----------------------------------------------
# Users parser
# -----------------------------------------------
user_parser = subparsers.add_parser(
    'user',
    help='Manage user account(s)',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''\
        A set of commands to manage CT8 accounts for automatic sign-in.
        All of below options can be run with multiple logins provided.
        When adding users you will be asked for passwords (they will be
        hidden from the prompt). 
        
        Examples:
        user --add john_smith, robert_maklowicz
        user --d john_smith
    '''),
)
user_parser.add_argument(
    '-a', '--add',
    action='store',
    nargs='+',
    help="add user's account to DB",
    metavar='login',
)
user_parser.add_argument(
    '--delete',
    action='store',
    nargs='+',
    help="delete user's user account from DB",
    metavar='login',
)
user_parser.add_argument(
    '-e', '--enable-account',
    action='store',
    nargs='+',
    help="enable user's account to automatic sign-in",
    metavar='login',
)
user_parser.add_argument(
    '-d', '--disable-account',
    action='store',
    nargs='+',
    help="disable user's account from automatic sign-in",
    metavar='login',
)
user_parser.add_argument(
    '-s', '--show-accounts',
    action='store_true',
    help='show all accounts stored in DB',
)
