import argparse


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
