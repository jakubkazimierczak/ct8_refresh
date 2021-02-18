from functools import partial

from loguru import logger
from peewee import OperationalError, IntegrityError, DoesNotExist
from rich.prompt import Prompt

from ct8_refresh import console
from ct8_refresh.account.model import Account

print_success = partial(console.print, style='green')
print_warning = partial(console.print, style='yellow')
print_error = partial(console.print, style='bright_red')


def catcher(operation='Operation'):
    def decorator(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except DoesNotExist as err:
                logger.error(err)
                print_error(f"{operation} failed: Account {args[0]} does not exists")
            except (OperationalError, IntegrityError) as err:
                logger.error(err)
                print_error(f"{operation} failed: {err}")

        return inner

    return decorator


def require_account(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DoesNotExist as err:
            logger.error(err)
            print_error(f'Account {args[0]} does not exists.')

    return inner


class AccountsManager:
    @staticmethod
    def exists(account_name):
        try:
            Account.get(Account.name == account_name)
            return True
        except DoesNotExist:
            return False

    @staticmethod
    @catcher('Getting account')
    def get_account(account_name) -> Account:
        return Account.get(Account.name == account_name)

    @staticmethod
    @catcher('Add')
    def add(account_name, password=None):
        if AccountsManager.exists(account_name):
            print_error(f'Cannot add {account_name} - account exists in DB.')
            return

        if not (password := password):
            password = Prompt.ask(f'{account_name} password', password=True)
        Account.create(name=account_name, password=password)
        print_success(f'Account {account_name} added.')

    @staticmethod
    @catcher('Delete')
    @require_account
    def delete(account_name):
        deleted = Account.delete().where(Account.name == account_name).execute()
        if deleted:
            print_success(f'Account {account_name} deleted')
        else:
            print_warning(f'Delete failed - account {account_name} not found.')

    @staticmethod
    @catcher('Changing active status')
    def set_active(account_name, value: bool):
        operation = 'enabled' if value else 'disabled'

        account = AccountsManager.get_account(account_name)
        account.is_active = value
        account.save()
        print_success(f'Account {operation} (automatic sign-in {operation}d).')

    @staticmethod
    @catcher('Updating expiration date')
    def update_expiration_date(account_name, date):
        account = AccountsManager.get_account(account_name)
        account.expires_on = date
        account.save()

    @staticmethod
    @catcher('Getting all accounts')
    def get_all_accounts():
        return Account.select()

    @staticmethod
    @catcher('Getting all accounts (sorted)')
    def get_all_accounts_sorted():
        return AccountsManager.get_all_accounts().order_by(
            Account.is_active.desc(), Account.expires_on
        )

    @staticmethod
    @catcher('Getting all active accounts')
    def get_active_accounts():
        return Account.select().where(Account.is_active)
