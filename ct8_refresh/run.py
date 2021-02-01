import sys

from loguru import logger
from pyppeteer import chromium_downloader
from rich import print
from rich.progress import BarColumn, Progress
from rich.prompt import Confirm

from . import console
from .account.manager import AccountsManager
from .account.model import Account
from .ct8 import CT8
from .ct8_pyppeteer import download_chromium


class Run:
    def __init__(self, all_users: bool):
        self.all_users = all_users

        self.progress = Progress(
            "[progress.description]{task.description}",
            BarColumn(),
            "{task.completed}/{task.total}",
        )

    @logger.catch
    def signin_loop(self):
        with self.progress:
            if self.all_users:
                users = AccountsManager.get_all_accounts()
            else:
                users = AccountsManager.get_active_accounts()
            if not users:
                sys.exit("No active users found. Please configure your users first.")

            task_id = self.progress.add_task("signin_check", total=len(users))
            self.progress.start_task(task_id)

            user: Account
            for user in users:
                self.progress.update(task_id, description=f"{user.name}: sign-in...")

                CT8(user.name, user.password, self.progress.console)

                self.progress.advance(task_id)

            self.progress.update(task_id, description=":100: Completed!")

    @logger.catch
    def main(self):
        if not chromium_downloader.check_chromium():
            print("A headless Chromium needs to be downloaded in order to continue.")
            console.print(
                "The download size is around [yellow]150MB[/yellow]. Proceed?"
            )
            if not Confirm.ask("Download and continue"):
                sys.exit(
                    "Script terminated - headless Chromium is necessary to run the script."
                )

            download_chromium()

        self.signin_loop()
