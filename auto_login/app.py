from auto_login.config import Config
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
def app():
    with progress:
        task_id = progress.add_task('signin_check', total=Config.load_users)
        progress.start_task(task_id)

        for user in Config.load_users():
            progress.update(task_id, description=f'{user.username}: sign-in...')

            ct8 = CT8(user.username, user.password, progress.console)
            if ct8.signed_in:
                ct8.get_expiry_date()

            progress.advance(task_id)

        progress.update(task_id, description=':100: Completed!')
