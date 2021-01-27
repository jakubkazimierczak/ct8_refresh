from auto_login.account.model import Account
from auto_login.account.manager import AccountsManager
from auto_login import console
from rich.table import Table


class AccountsView:
    @staticmethod
    def show_accounts():
        table = Table(title='Users')
        table.add_column('Name')
        table.add_column('Enabled')
        table.add_column('Expires on')

        accounts = AccountsManager.get_all_accounts().order_by(Account.is_active.desc())
        account: Account
        for account in accounts:
            table.add_row(account.name, str(account.is_active), account.expires_on)

        console.print(table)
