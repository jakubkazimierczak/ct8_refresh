from rich.prompt import Prompt
from auto_login import console
from loguru import logger
from peewee import OperationalError, IntegrityError
from auto_login.account.model import Account
from functools import partial


print_success = partial(console.print, style='green')
print_warning = partial(console.print, style='yellow')
print_error = partial(console.print, style='bright_red')


class AccountsManager:
    @staticmethod
    def _exists(account_name):
        account = Account.select(Account.name).where(Account.name == account_name)
        return list(account)

    @staticmethod
    def add(account_name):
        if AccountsManager._exists(account_name):
            console.print(f'Cannot add {account_name} - account exists in DB.', style='bright_red')
            return

        password = Prompt.ask(f'{account_name} password', password=True)
        try:
            Account.insert(name=account_name, password=password).execute()
            print_success('Account added.')
        except (OperationalError, IntegrityError) as err:
            logger.error(err)
            console.print(f'Failed to add user: {err}', style='bold red')

    @staticmethod
    def delete(account_name):
        try:
            deleted = Account.delete().where(Account.name == account_name).execute()
            if deleted:
                print_success('Account deleted')
            else:
                print_warning('Account not found.')
        except (OperationalError, IntegrityError) as err:
            logger.error(err)
            console.print(f'Failed to remove user: {err}', style='bold red')

    @staticmethod
    def _set_account_status(account_name, value=True):
        Account\
            .update({Account.is_active: value})\
            .where(Account.name == account_name)\
            .execute()

    @staticmethod
    def enable(account_name):
        try:
            AccountsManager._set_account_status(account_name, True)
            print_success('Account enabled. Automatic sign-in will be performed on future runs.')
        except (OperationalError, IntegrityError) as err:
            logger.error(err)
            console.print(f"Failed to enable account: {err}", style='bold red')

    @staticmethod
    def disable(account_name):
        try:
            AccountsManager._set_account_status(account_name, False)
            print_success("Account disabled. Automatic sign-in won't be performed on future runs.")
        except (OperationalError, IntegrityError) as err:
            logger.error(err)
            console.print(f"Failed to disable account: {err}", style='bold red')

    @staticmethod
    def get_all_accounts():
        return Account.select()

    @staticmethod
    def get_active_accounts():
        return Account.select().where(Account.is_active)


if __name__ == '__main__':
    acc: Account
    for acc in AccountsManager.get_active_accounts():
        print(acc.name)
