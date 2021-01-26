from auto_login.config import Config
from auto_login.account.model import Account
from auto_login.account.manager import AccountsManager
from auto_login.ct8 import CT8
from loguru import logger
from rich.progress import (
    BarColumn,
    Progress
)


progress = Progress(
    "[progress.description]{task.description}",
    BarColumn(),
    "{task.completed}/{task.total}",
)


@logger.catch
def signin_loop():
    with progress:
        users = AccountsManager.get_active_accounts()
        task_id = progress.add_task('signin_check', total=len(users))
        progress.start_task(task_id)

        user: Account
        for user in users:
            progress.update(task_id, description=f'{user.name}: sign-in...')

            ct8 = CT8(user.name, user.password, progress.console)
            if ct8.signed_in:
                ct8.get_expiration_date()

            progress.advance(task_id)

        progress.update(task_id, description=':100: Completed!')