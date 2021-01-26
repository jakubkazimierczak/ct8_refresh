from loguru import logger
from peewee import OperationalError, IntegrityError


@logger.catch(exclude=(OperationalError, IntegrityError))
def main():
    try:
        import auto_login.cli
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
