from auto_login.config import Config
from auto_login.ct8_manager import CT8_manager


def app():
    for user in Config.load_users():
        ct8 = CT8_manager(user.username, user.password)
        ct8.get_expiry_date()
