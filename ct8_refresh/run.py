import sys

from loguru import logger
from rich.progress import BarColumn, Progress

from .account.manager import AccountsManager
from .account.model import Account
from .ct8 import CT8


class Run:
    def __init__(self, all_users: bool):
        self.all_users = all_users

        self.progress = Progress(
            '[progress.description]{task.description}',
            BarColumn(),
            '{task.completed}/{task.total}',
        )

    @logger.catch
    def signin_loop(self):
        with self.progress:
            if self.all_users:
                users = AccountsManager.get_all_accounts()
            else:
                users = AccountsManager.get_active_accounts()
            if not users:
                sys.exit('No active users found. Please configure your users first.')

            task_id = self.progress.add_task('signin_check', total=len(users))
            self.progress.start_task(task_id)

            user: Account
            for user in users:
                self.progress.update(task_id, description=f'{user.name}: sign-in...')

                ct8_user = CT8(user.name, user.password)
                result = ct8_user.sign_in_request()
                ct8_user.update_expiration_date()
                self.progress.console.print(result)

                self.progress.advance(task_id)

            self.progress.update(task_id, description=':100: Completed!')

    @logger.catch
    def main(self):
        self.signin_loop()
