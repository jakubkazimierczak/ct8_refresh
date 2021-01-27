from ct8_refresh.account.model import Account
from ct8_refresh.account.manager import AccountsManager
from ct8_refresh import console
from rich.table import Table
from datetime import datetime


class AccountsView:
    @staticmethod
    def get_row_style(days_remaining):
        if days_remaining < 30:
            return 'red'
        elif days_remaining < 60:
            return 'yellow'
        elif days_remaining < 90:
            return 'green'
        else:
            return None

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
            # Calculate expiration date
            expires_in, style = '', None
            if account.expires_on:
                expires_in = datetime.fromisoformat(str(account.expires_on)) - datetime.today()
                style = AccountsView.get_row_style(expires_in.days)
                expires_in = str(expires_in.days)

            table.add_row(account.name, str(account.is_active), str(account.expires_on)[:-7], str(expires_in), style=style)

        console.print(table)
