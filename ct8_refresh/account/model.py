from loguru import logger

from ct8_refresh import DATABASE_PATH

from peewee import (
    Model,
    SqliteDatabase,
    BooleanField,
    CharField,
    DateTimeField,
)


logger.debug('Database path: {}'.format(DATABASE_PATH))
database = SqliteDatabase(DATABASE_PATH)


class Account(Model):
    name = CharField(primary_key=True)
    password = CharField()
    is_active = BooleanField(default=True)
    expires_on = DateTimeField(null=True)

    class Meta:
        database = database


def create_tables():
    with database:
        database.create_tables([Account])
