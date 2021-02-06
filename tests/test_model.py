from datetime import datetime, timedelta

import pytest

from ct8_refresh.account.model import Account


@pytest.fixture
def account() -> Account:
    expires_on = datetime.today() + timedelta(days=90)
    return Account(
        name='john', password='password123', is_active=True, expires_on=expires_on
    )


def test_expire_date(account):
    account.expires_on = datetime(2012, 2, 29, 12, 34, 56, 789)
    assert account.expire_date == '2012-02-29 12:34:56'


@pytest.mark.parametrize(
    'days, expected',
    [(0, 0), (27, 27), (90, 90)],
)
def test_expires_in(days, expected, account):
    account.expires_on = datetime.today() + timedelta(days=days)
    assert account.expires_in == expected


def test_expires_in_none(account):
    account.expires_on = None
    assert account.expires_in == 0


@pytest.mark.parametrize(
    'days, expected',
    [(0, 'red'), (28, 'red'), (30, 'yellow'), (52, 'yellow'), (78, 'green')],
)
def test_row_style(days, expected, account):
    account.expires_on = datetime.today() + timedelta(days=days)
    assert account.row_style == expected
