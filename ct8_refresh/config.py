from collections import namedtuple
from loguru import logger


class Config:
    @staticmethod
    def load_users():
        User = namedtuple('User', 'username password')
        users = []

        try:
            with open('logins.txt', 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            logger.critical('Config file not found! ')

        usernames = lines[::2]
        passwords = lines[1::2]
        for username, password in zip(usernames, passwords):
            user = User(username.strip(), password.strip())
            users.append(user)

        return users

    @property
    def user_count(self) -> int:
        return len(self.load_users())
