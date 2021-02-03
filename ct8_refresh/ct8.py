from datetime import datetime, timedelta

from loguru import logger
from requests import Session

from .account.manager import AccountsManager
from .constants import SIGNIN_URL


class CT8:
    def __init__(self, username, password, progress_console=None):
        self.username = username
        self.password = password
        self.signed_in = False
        self.session = Session()
        self._console = progress_console

    @staticmethod
    def _prepare_header(csrf_token):
        return {
            'Host': 'panel.ct8.pl',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.50',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': '139',
            'Origin': 'https://panel.ct8.pl',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Referer': 'https://panel.ct8.pl/login/',
            'Cookie': f'csrftoken={csrf_token}',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }

    def sign_in_request(self):
        self.session.get(SIGNIN_URL)
        csrf_token = self.session.cookies.get('csrftoken')

        headers = self._prepare_header(csrf_token)
        login_data = {
            'csrfmiddlewaretoken': csrf_token,
            'username': self.username,
            'password': self.password,
        }

        # Sign-in
        res = self.session.post(
            SIGNIN_URL, data=login_data, headers=headers, allow_redirects=False
        )
        if res.status_code == 302:
            if res.next:
                self.session.send(res.next)
            self.signed_in = True
            logger.debug('Signed in as {}', self.username)
            if self._console:
                self._console.print(f':heavy_check_mark: Signed in as {self.username}')
        else:
            logger.warning(
                'Login failed for {}. Check the login credentials and try again.',
                self.username,
            )
            if self._console:
                self._console.print(
                    f':x: Login failed for {self.username}. Check the login credentials and try again.'
                )

    def update_expiration_date(self):
        if self.signed_in:
            expires_on = datetime.today() + timedelta(days=90)
            AccountsManager.update_expiration_date(self.username, expires_on)

    def sign_in(self):
        self.sign_in_request()
        self.update_expiration_date()
