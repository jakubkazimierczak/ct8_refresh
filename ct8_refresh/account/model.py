from peewee import (
    Model,
    SqliteDatabase,
    BooleanField,
    CharField,
    # DateField,
    DateTimeField,
)


database = SqliteDatabase('accounts.db')


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
