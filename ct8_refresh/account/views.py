from rich.table import Table

from ct8_refresh import console
from ct8_refresh.account.manager import AccountsManager
from ct8_refresh.account.model import Account


class AccountsView:
    @staticmethod
    def show_accounts():
        table = Table(title='Users')
        table.add_column('Name')
        table.add_column('Enabled')
        table.add_column('Expires on')
        table.add_column('Remaining days')

        accounts = AccountsManager.get_all_accounts().order_by(Account.is_active.desc(), Account.expires_on)
        account: Account
        for account in accounts:
            table.add_row(account.name, str(account.is_active), account.expire_date, str(account.expires_in), style=account.row_style)

        console.print(table)
