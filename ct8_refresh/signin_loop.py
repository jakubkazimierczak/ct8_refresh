from ct8_refresh.account.model import Account
from ct8_refresh.account.manager import AccountsManager
from ct8_refresh.ct8 import CT8
import sys
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
        if not users:
            sys.exit('No active users found. Please configure your users first.')

        task_id = progress.add_task('signin_check', total=len(users))
        progress.start_task(task_id)

        user: Account
        for user in users:
            progress.update(task_id, description=f'{user.name}: sign-in...')

            ct8 = CT8(user.name, user.password, progress.console)

            progress.advance(task_id)

        progress.update(task_id, description=':100: Completed!')
