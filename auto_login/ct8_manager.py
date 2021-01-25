from loguru import logger
from requests_html import HTMLSession


class CT8_manager:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.signed_in = False
        self.session = HTMLSession()

        self.sign_in()

    @staticmethod
    def _headers(csrf_token):
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
            'Cache-Control': 'no-cache'
        }

    def sign_in(self):
        url = 'https://panel.ct8.pl/login/'
        r = self.session.get(url)
        r.html.render()
        csrf_token = self.session.cookies.get('csrftoken')

        headers = self._headers(csrf_token)
        login_data = {
            'csrfmiddlewaretoken': csrf_token,
            'username': self.username,
            'password': self.password
        }

        # Sign-in
        r = self.session.post(url, data=login_data, headers=headers)
        if len(r.history) and r.history[0].status_code == 302:
            self.signed_in = True
            logger.debug('Signed in as {}', self.username)
        else:
            logger.error('Login failed for {}', self.username)

    def get_expiry_date(self):
        if not self.signed_in:
            logger.error('User must be signed in to perform this action')
            return

        # Get expiry info
        r = self.session.get('https://panel.ct8.pl/dashboard')
        if r.status_code == 200:
            if 'Konto ważne do' in r.text or 'Expiration date' in r.text:
                expiry = r.html.find('.well', first=True).text.split('\n')[-1]

                logger.debug('Expiry info found on page')
                logger.info('{} expires on {}', self.username, expiry)

                return expiry
        else:
            logger.error('Could not query account info')
