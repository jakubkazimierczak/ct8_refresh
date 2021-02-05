from datetime import datetime
from typing import Union

from loguru import logger
from peewee import (
    Model,
    SqliteDatabase,
    BooleanField,
    CharField,
    DateTimeField,
)

from ct8_refresh import DATABASE_PATH

logger.debug('Database path: {}'.format(DATABASE_PATH))
database = SqliteDatabase(DATABASE_PATH)


class Account(Model):
    name = CharField(primary_key=True)
    password = CharField()
    is_active = BooleanField(default=True)
    expires_on = DateTimeField(null=True)

    class Meta:
        database = database

    @property
    def expire_date(self) -> str:
        return str(self.expires_on)[:-7]

    @property
    def expires_in(self) -> int:
        if self.expires_on:
            delta = datetime.fromisoformat(str(self.expires_on)) - datetime.today()
            return delta.days
        else:
            return 0

    @property
    def row_style(self) -> Union[str, None]:
        days_remaining = self.expires_in
        if days_remaining < 30:
            return 'red'
        elif days_remaining < 60:
            return 'yellow'
        else:  # days_remaining < 90
            return 'green'


def create_tables():
    with database:
        database.create_tables([Account])
